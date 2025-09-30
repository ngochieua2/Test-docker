import base64
from uuid import UUID
import pandas as pd
from fastapi import APIRouter, Body, HTTPException, Query, Request

from app.core.state import connections

import json
from fastapi.responses import StreamingResponse
from confluent_kafka import  Consumer
import asyncio

from app.config import settings

from app.dependencies.db_context import DbContext
from app.api.v1.endpoints.chats.requests.chat_message import ChatMessageCreateRequest
from app.schemas.queries.query_chat_threads import (
    get_chat_threads_by_user_id_query,
    get_chat_threads_by_user_id_query_handler_async,
)
from app.schemas.queries.query_chat_messages_by_chat_thread_id import (
    get_chat_messages_by_chat_thread_id_query, 
    get_chat_messages_by_chat_thread_id_query_handler_async,
    get_import_data_by_chat_thread_id_query_handler_async,
)
from app.schemas.commands.command_create_chat_thread import (
    create_chat_thread_command,
    create_chat_thread_command_handler_async,
)
from app.schemas.commands.command_create_chat_message import (
    create_chat_message_command,
    create_chat_message_command_response,
    create_chat_message_command_handler_async,
)

# ImportData module
from .requests.import_data_request import ImportDataRequest
from .responses.import_data_response import ImportProfileResponse
from app.schemas.commands.command_import_data import GetImportDataResponse, import_data_from_bytes, get_import_data_by_user_id

router = APIRouter()


# SSE stream endpoint
@router.get("/{user_id}/threads/{chat_thread_id}/connect")
async def stream(
    request: Request,
    user_id: UUID,
    chat_thread_id: UUID
):
    key = f"{user_id}:{chat_thread_id}"
    queue = asyncio.Queue()

    if key not in connections:
        connections[key] = []

    connections[key].append(queue)

    async def event_generator():
        try:
            while True:
                # If client disconnected, break and cleanup
                if await request.is_disconnected():
                    break

                try:
                    item, kafka_msg = await queue.get()
                    print(f"GOT from queue: {item}")
                    # Unpack properly in case of local message
                    if isinstance(item, tuple) and len(item) == 2:
                        data, kafka_msg = item
                    else:
                        data, kafka_msg = item, None
                except asyncio.CancelledError:
                    break

                if hasattr(item, "model_dump"):
                    data = item.model_dump()
                else:
                    data = item

                yield f"data: {json.dumps(data)}\n\n"

                if kafka_msg:
                    try:
                        consumer: Consumer = request.app.state.kafka_consumer
                        consumer.commit(kafka_msg, asynchronous=False)
                        print(f"Committed offset: {kafka_msg.topic()}-{kafka_msg.partition()}@{kafka_msg.offset()}")
                    except Exception as e:
                        print("Commit error:", e)
                else:
                    print(f"Skipped commit (local message)")

        finally:
            connections[key].remove(queue)
            if not connections[key]:
                del connections[key]

    return StreamingResponse(event_generator(), media_type="text/event-stream")

# ===================== CHAT ENDPOINTS =====================

@router.get("/{user_id}/threads")
async def get_chat_threads_async(dbContext: DbContext, user_id: UUID):
    query = get_chat_threads_by_user_id_query(user_id=user_id)
    chat_threads = await get_chat_threads_by_user_id_query_handler_async(dbContext, query)
    if chat_threads is None:
        raise HTTPException(
            status_code=400,
            detail={
                "status": 400,
                "errors": [
                    {"status": 4001, "message": "Failure to create chat thread!"}
                ],
            },
        )
    return {"status": 200, "data": chat_threads}


@router.get("/{user_id}/threads/{chat_thread_id}/chats")
async def get_chat_messages_async(dbContext: DbContext, user_id: UUID, chat_thread_id: UUID):
    query = get_chat_messages_by_chat_thread_id_query(user_id=user_id, id=chat_thread_id)
    chat_threads = await get_chat_messages_by_chat_thread_id_query_handler_async(dbContext, query)
    if chat_threads is None:
        raise HTTPException(
            status_code=400,
            detail={
                "status": 400,
                "errors": [{"status": 4001, "message": "Not found chat messages"}],
            },
        )
    return {"status": 200, "data": chat_threads}

@router.get("/{user_id}/threads/{chat_thread_id}/import-datas")
async def get_chat_messages_async(dbContext: DbContext, user_id: UUID, chat_thread_id: UUID):
    query = get_chat_messages_by_chat_thread_id_query(user_id=user_id, id=chat_thread_id)
    chat_threads = await get_import_data_by_chat_thread_id_query_handler_async(dbContext, query)
    if chat_threads is None:
        raise HTTPException(
            status_code=400,
            detail={
                "status": 400,
                "errors": [{"status": 4001, "message": "Not found import data."}],
            },
        )
    return {"status": 200, "data": chat_threads}


@router.post("/{user_id}/threads")
async def create_new_thread_async(dbContext: DbContext, user_id: UUID):
    command = create_chat_thread_command(user_id=user_id)
    chat_thread = await create_chat_thread_command_handler_async(dbContext, command)
    if chat_thread is None:
        return {"status": 400}
    return {"status": 200, "chat_thread_id": chat_thread.id}


@router.post("/{user_id}/threads/{chat_thread_id}/chats")
async def create_new_message_async(
    request: Request,
    dbContext: DbContext, 
    user_id: UUID, 
    chat_thread_id: UUID, 
    chat_request: ChatMessageCreateRequest
):
    command = create_chat_message_command(
        user_id=user_id, chat_thread_id=chat_thread_id, message=chat_request.message
    )
    chat_message: create_chat_message_command_response  = await create_chat_message_command_handler_async(dbContext, command)
    """User A sends a message to User B."""
    receive_message = {"user_id": str(user_id), "chat_thread_id": str(chat_thread_id), "message": json.dumps(chat_message.model_dump())}
    producer = request.app.state.kafka_producer
    producer.produce(settings.KAFKA_TOPIC, json.dumps(receive_message).encode("utf-8"))
    producer.flush()

    return {"status": 200}


# ===================== IMPORT DATA ENDPOINT =====================

@router.post(
    "/import-data",
    response_model=ImportProfileResponse,
    summary="Import + profile a CSV/XLS/XLSX from base64 bytes",
)
async def import_data_async(
    request: ImportDataRequest = Body(...),
    distributions_format: str = Query("list", enum=["list", "dataframe"]),
    save_profile_json: bool = Query(False),
    profile_field_name: str = Query("ProfileJson"),
):
    raw_b64 = request.file_base64.split(",", 1)[-1]
    try:
        file_content = base64.b64decode(raw_b64, validate=True)
    except Exception:
        raise HTTPException(status_code=400, detail="File decode failed")

    try:
        result = await import_data_from_bytes(
            file_content,
            filename=request.filename,
            fileUrl=request.fileUrl,
            threadId =request.thread_id,
            user_id=request.user_id,
            distributions_format=distributions_format,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to import & profile file")

    # Ensure JSON-safe for distributions if user requested "dataframe"
    if distributions_format == "dataframe":
        dist = result.get("distributions")
        if isinstance(dist, pd.DataFrame):
            result["distributions"] = (
                dist.astype(object).where(pd.notna(dist), None).to_dict(orient="records")
            )

    return ImportProfileResponse(
        filename=request.filename,
        import_record_id=result.pop("_import_record_id", None),
        data_summary=result.pop("data_summary", None),
        suggestions=result.pop("suggestions", []),
        data_preview=result.pop("preview_rows")
    )

@router.get("/import-data/{user_id}", response_model=GetImportDataResponse)
async def get_import_data(user_id: UUID):
    return await get_import_data_by_user_id(user_id)

