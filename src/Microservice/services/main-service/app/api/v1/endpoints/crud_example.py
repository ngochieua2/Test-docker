from typing import List, Optional
from fastapi import APIRouter, HTTPException, Depends, Query
from shared.utils import get_logger
from app.repository.crud_example_repository import CrudExampleRepository
from app.services.crud_example_service import CrudExampleService
from app.schemas.crudExample import CrudExampleResponse, CrudExampleCreate, CrudExampleUpdate
from sqlalchemy.orm import Session
from shared.database.dbContext import get_db

logger = get_logger(__name__)
router = APIRouter()

# Dependency injection for repository and service
def get_crud_example_repository() -> CrudExampleRepository:
    """Get CrudExampleRepository instance"""
    return CrudExampleRepository()

def get_crud_example_service(
    crud_example_repository: CrudExampleRepository = Depends(get_crud_example_repository)
    ) -> CrudExampleService:
    """Get CrudExampleService instance with injected repository"""
    return CrudExampleService(crud_example_repository)

@router.get("/search", response_model=List[CrudExampleResponse])
async def search_crud_examples(
    skip: int = Query(0, ge=0, description="Number of examples to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of examples to return"),
    isActive: Optional[bool] = Query(None, description="Filter by active status"),
    status: Optional[int] = Query(None, description="Filter by status code"),
    search: Optional[str] = Query(None, description="Filter by search term"),
    db: Session = Depends(get_db),
    crud_example_service: CrudExampleService = Depends(get_crud_example_service)
):
    """
    Get all crud examples with optional filtering and pagination
    """
    logger.info(f"Fetching crud examples: skip={skip}, limit={limit}, isActive={isActive}, status={status}, search={search}")
    return await crud_example_service.search_crud_examples(
        db=db,
        skip=skip,
        limit=limit,
        isActive=isActive,
        status=status,
        search=search
    )

@router.get("/{example_id}", response_model=CrudExampleResponse)
async def get_crud_example_detail(
    example_id: int,
    db: Session = Depends(get_db),
    crud_example_service: CrudExampleService = Depends(get_crud_example_service)
):
    """
    Get a single crud example by ID
    """
    logger.info(f"Fetching crud example: id={example_id}")

    crud_example = await crud_example_service.get_crud_example_detail(
        db=db,
        example_id=example_id
    )

    if not crud_example:
        logger.warning(f"Crud example not found: id={example_id}")
        raise HTTPException(status_code=400, detail="Crud example not found")
    return crud_example

@router.post("/", response_model=CrudExampleResponse, status_code=201)
async def create_crud_example(
    example_data: CrudExampleCreate,
    db: Session = Depends(get_db),
    crud_example_service: CrudExampleService = Depends(get_crud_example_service)
):
    """
    Create a new crud example
    """
    logger.info(f"Creating new crud example: {example_data.name}")
    return await crud_example_service.create_crud_example(
        db=db,
        crud_example_data=example_data
    )

@router.put("/", response_model=CrudExampleResponse)
async def update_crud_example(
    example_id: int,
    example_data: CrudExampleUpdate,
    db: Session = Depends(get_db),
    crud_example_service: CrudExampleService = Depends(get_crud_example_service)
):
    """
    Update an existing crud example
    """
    logger.info(f"Updating crud example: id={example_id}")
    updated_example = await crud_example_service.update_crud_example(
        db=db,
        example_id=example_id,
        crud_example_update=example_data
    )
    if not updated_example:
        logger.warning(f"Crud example not found for update: id={example_id}")
        raise HTTPException(status_code=400, detail="Crud example not found")
    return updated_example

@router.delete("/{example_id}", status_code=204)
async def delete_crud_example(
    example_id: int,
    db: Session = Depends(get_db),
    crud_example_service: CrudExampleService = Depends(get_crud_example_service)
):
    """
    Delete a crud example by ID
    """
    logger.info(f"Deleting crud example: id={example_id}")
    success = await crud_example_service.delete_crud_example(
        db=db,
        example_id=example_id
    )
    if not success:
        logger.warning(f"Crud example not found for deletion: id={example_id}")
        raise HTTPException(status_code=400, detail="Crud example not found")
    return