import json
from pprint import pprint
import uuid
import io
from typing import Any, Dict, List, Literal, Optional
import pandas as pd
import numpy as np
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import insert,select
from app.schemas.queries.query_chat_messages_by_chat_thread_id import import_data_dto
from app.services import chat_service
from app.models.import_data import ImportData, ImportStatus
from app.core.utils.datetime_utils import now_utc
from app.config import settings   # to get DATABASE_URL
from app.models.chat_thread import ChatThread
from app.models.user import User
# ================================================================
# Command and Response Models for external use


class GetImportDataResponse(BaseModel):
    import_data: List[import_data_dto]
# ================================================================

# ================================================================
# Setup DB session factory (defined here to avoid extra file)

engine = create_async_engine(settings.SQLALCHEMY_DATABASE_URI, echo=True, future=True)
async_session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

# ================================================================


# ================================================================
# Public Service
async def import_data_from_bytes(
    file_bytes: bytes,
    filename: str,
    fileUrl: str,
    threadId: uuid.UUID,
    user_id: uuid.UUID,    
    *,
    distributions_format: Literal["list", "dataframe"] = "list",
    known_keys: Optional[List[str]] = None,
    breakdown_key: Optional[str] = "requestType",
) -> Dict[str, Any]:
    """
    Import a CSV/XLS/XLSX file from raw bytes, profile its content,
    and record the operation in the ImportData table.
    """

    record_id = uuid.uuid4()

    async with async_session() as db_session:
        try:
            # 🔹 Validate threadId
            chatThread = await db_session.get(ChatThread, (threadId, user_id))
            if chatThread is None:
                raise ValueError(f"ChatThread with id {threadId} not found.")

            # 🔹 Validate user
            user = await db_session.get(User, user_id)
            if user is None:
                raise ValueError(f"User with id {user_id} not found.")

            # 0) Insert ImportData record (initially PENDING)
            stmt = (
                insert(ImportData)
                .values(
                    Id=record_id,
                    FileName=filename,
                    FileUrl=fileUrl,
                    Status=ImportStatus.PENDING,
                    ThreadId=threadId,
                    UserId=user_id,
                    CreatedBy=user_id,
                    CreatedOn=now_utc(),
                    LastModifiedBy=user_id,
                    LastModifiedOn=now_utc(),
                )
                .returning(ImportData)
            )
            result = await db_session.execute(stmt)
            await db_session.commit()
            record = result.scalar_one_or_none()

            # 1) Detect file type
            file_type = _detect_file_type(file_bytes)
            try:
                if file_type == ".csv":
                    df = pd.read_csv(io.BytesIO(file_bytes), encoding="utf-8", errors="ignore")
                elif file_type == ".xlsx":
                    df = pd.read_excel(io.BytesIO(file_bytes), engine="openpyxl")
                elif file_type == ".xls":
                    df = pd.read_excel(io.BytesIO(file_bytes), engine="xlrd")
                else:
                    raise ValueError("Unsupported file format. Use .csv, .xlsx, or .xls")
            except Exception as e:
                raise ValueError(f"Failed to parse file: {str(e)}")

            # 2) Clean DataFrame
            df = _clean_dataframe(df)

            # 3) Build profiling information
            result_dict: Dict[str, Any] = {
                "preview_rows": _preview_first_rows(df, n=10),
                "overview": {
                    "file_path": fileUrl,
                    "total_records": int(len(df)),
                    "columns": [str(c) for c in df.columns],
                },
                "column_details": _per_column_details(df),
                "distributions": (
                    pd.DataFrame(_distribution_summary_list(df))
                    if distributions_format == "dataframe"
                    else _distribution_summary_list(df)
                ),
                "known_dimensions": _known_dimension_distributions(df, known_keys),
                "request_type_breakdown": _generic_breakdown(df, breakdown_key) if breakdown_key else None,
                "_import_record_id": str(record.Id) if record else str(record_id),
            }

            result_dict = _to_native(result_dict)

            summarizeDataResult = await chat_service.excute_gpt_chat_async(
                prompt = settings.IMPORT_DATA_PROMPT,
                content=json.dumps(result_dict, ensure_ascii=False)
            )
            
            fullDataSummary : str
            dataSummary : str
            suggestions : List[str]
            try:
                fullDataSummary = json.loads(summarizeDataResult.response)
                dataSummary = fullDataSummary.get("data_summary", "")
                suggestions = fullDataSummary.get("suggestions", [])
            except Exception:
                dataSummary = summarizeDataResult.response
                suggestions = []

            # 5) Update ImportData status to COMPLETED
            if isinstance(fullDataSummary, dict):
                record.DataSummary = json.dumps(fullDataSummary, ensure_ascii=False)
            else:
                record.DataSummary = str(fullDataSummary)

            record.Status = ImportStatus.COMPLETED
            record.LastModifiedOn = now_utc()            
            record.Response = json.dumps(result_dict, ensure_ascii=False)            
            db_session.add(record)
            await db_session.commit()
            
            result_dict["data_summary"] = dataSummary
            result_dict["suggestions"] = suggestions

            return result_dict

        except ValueError as ve:
            # 🔹 Raise 400-friendly error
            raise ve

        except Exception as e:
            # 🔹 Handle failure: log + mark FAILED in DB
            import traceback
            print("❌ import_data_from_bytes failed:", repr(e))
            traceback.print_exc()
            try:
                await db_session.execute(
                    insert(ImportData).values(
                        Id=record_id,
                        FileName=filename,
                        FileUrl=fileUrl,
                        Status=ImportStatus.FAILED,
                        UserId=user_id,
                        CreatedBy=user_id,
                        CreatedOn=now_utc(),
                        LastModifiedBy=user_id,
                        LastModifiedOn=now_utc(),
                    )
                )
                await db_session.commit()
            finally:
                raise


async def get_import_data_by_user_id(user_id: uuid.UUID) -> GetImportDataResponse:
    async with async_session() as session:
        query = (
            select(ImportData)
            .where(
                ImportData.UserId == user_id,
                ImportData.Status == ImportStatus.COMPLETED.value
            )
            .order_by(ImportData.CreatedOn.desc())
        )
        result = await session.execute(query)
        records = result.scalars().all()

        dto_records = []
        for r in records:
            # 🔹 Parse Response -> lấy data_preview
            data_preview = []
            try:
                if r.Response:
                    response_obj = json.loads(r.Response)
                    if isinstance(response_obj, dict):
                        data_preview = response_obj.get("preview_rows", [])
            except Exception:
                data_preview = []

            # 🔹 Parse DataSummary JSON -> lấy data_summary + suggestions
            data_summary = ""
            suggestions = []
            try:
                if r.DataSummary:
                    parsed_summary = json.loads(r.DataSummary)
                    data_summary = parsed_summary.get("data_summary", "")
                    suggestions = parsed_summary.get("suggestions", [])
            except Exception:
                data_summary = r.DataSummary or ""
                suggestions = []

            # 🔹 Build DTO
            dto_records.append(
                import_data_dto(
                    id=str(r.Id),
                    user_id=r.UserId,
                    file_name=r.FileName,
                    file_url=r.FileUrl,
                    status=r.Status,
                    data_preview=data_preview,
                    data_summary=data_summary,
                    suggestions=suggestions
                )
            )

        return GetImportDataResponse(import_data=dto_records)



# ================================================================

# ================================================================
# Helpers
# ================================================================
def _to_native(obj: Any) -> Any:
    """Convert numpy/pandas objects into JSON-serializable Python types."""
    if isinstance(obj, (pd.Series, pd.DataFrame)):
        return obj.astype(object).where(pd.notna(obj), None).to_dict(orient="records")
    if isinstance(obj, (pd.Timestamp, pd.Timedelta)):
        return obj.isoformat()
    if isinstance(obj, (np.integer,)):
        return int(obj)
    if isinstance(obj, (np.floating,)):
        return float(obj)
    if isinstance(obj, (np.ndarray,)):
        return obj.tolist()
    if isinstance(obj, dict):
        return {str(k): _to_native(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_to_native(v) for v in obj]
    return obj


def _detect_file_type(file_bytes: bytes) -> str:
    """Detect file type by inspecting file magic bytes."""
    if file_bytes[:4] == b"PK\x03\x04":
        return ".xlsx"
    if file_bytes[:8] == b"\xD0\xCF\x11\xE0\xA1\xB1\x1A\xE1":
        return ".xls"
    return ".csv"


def _clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Remove empty rows/columns and strip column names."""
    df = df.copy()
    df.dropna(how="all", inplace=True)
    df.dropna(axis=1, how="all", inplace=True)
    df.columns = [str(c).strip() for c in df.columns]
    return df


def _preview_first_rows(df: pd.DataFrame, n: int = 10) -> List[Dict[str, str]]:
    """Return first n rows as list of dictionaries (stringified)."""
    if df.empty:
        return []
    head = df.head(n).copy().fillna("")
    for c in head.columns:
        head[c] = head[c].astype(str)
    return head.to_dict(orient="records")


def _per_column_details(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """Build per-column summary: dtype, uniqueness, nulls, min/max, datetime range."""
    details: List[Dict[str, Any]] = []
    for col in df.columns:
        ser = df[col]
        info: Dict[str, Any] = {
            "name": str(col),
            "dtype": str(ser.dtype),
            "unique": bool(ser.is_unique),
            "samples": ser.dropna().astype(str).unique()[:3].tolist(),
            "nulls": int(ser.isnull().sum()),
        }
        if pd.api.types.is_numeric_dtype(ser) and not ser.isnull().all():
            info["numeric"] = True
            info["min"] = _to_native(ser.min())
            info["max"] = _to_native(ser.max())
        name_l = str(col).lower()
        if pd.api.types.is_datetime64_any_dtype(ser) or ("time" in name_l) or ("date" in name_l):
            try:
                parsed = pd.to_datetime(ser, errors="coerce", utc=False)
                if parsed.notna().any():
                    info["datetime"] = True
                    info["date_min"] = parsed.min().isoformat()
                    info["date_max"] = parsed.max().isoformat()
                else:
                    info["datetime"] = False
                    info["note"] = "Could not parse any values as datetime."
            except Exception:
                info["datetime"] = False
                info["note"] = "Datetime parsing failed."
        details.append(info)
    return details


def _distribution_summary_list(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """Build per-column frequency distributions (unique count, median frequency, top 3 values)."""
    out: List[Dict[str, Any]] = []
    for col in df.columns:
        ser = df[col]
        vc = ser.value_counts(dropna=True)
        out.append({
            "Column": str(col),
            "Unique Values": int(ser.nunique(dropna=True)),
            "Median Frequency": float(vc.median()) if not vc.empty else None,
            "Top 3 Most Common": {str(k): int(v) for k, v in vc.head(3).items()},
        })
    return out


def _known_dimension_distributions(df: pd.DataFrame, keys: Optional[List[str]] = None) -> Dict[str, Any]:
    """Build distribution summaries for known dimension keys (if present)."""
    keys = keys or ["imsi", "subscriptionId", "offerName", "zone", "requestType", "mccmnc"]
    res: Dict[str, Any] = {}
    for k in keys:
        if k in df.columns:
            vc = df[k].value_counts(dropna=True)
            res[k] = {
                "unique": int(df[k].nunique(dropna=True)),
                "count_non_null": int(df[k].count()),
                "top5": {str(a): int(b) for a, b in vc.head(5).items()},
            }
    return res


def _generic_breakdown(df: pd.DataFrame, col_name: str) -> Optional[Dict[str, int]]:
    """Build breakdown frequency distribution for a given column (if exists)."""
    if col_name not in df.columns:
        return None
    vc = df[col_name].value_counts(dropna=True)
    return {str(k): int(v) for k, v in vc.items()}



