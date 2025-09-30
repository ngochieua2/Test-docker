from typing import Optional, List
from sqlalchemy.orm import Session
from shared.utils.logger import get_logger
from app.repository.crud_example_repository import CrudExampleRepository
from app.schemas.crudExample import CrudExampleResponse, CrudExampleCreate, CrudExampleUpdate

logger = get_logger(__name__)

class CrudExampleService:
    """
    Business logic for crud example operations using repository pattern
    """
    def __init__(self, crud_example_repository: CrudExampleRepository = None):
        self.crud_example_repository = crud_example_repository or CrudExampleRepository()

    async def search_crud_examples(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
        isActive: Optional[bool] = None,
        status: Optional[int] = None,
        search: Optional[str] = None
    ) -> List[CrudExampleResponse]:
        """
        Search crud examples with optional filtering
        """
        # Use repository for database operations
        crud_examples = self.crud_example_repository.search_crud_example(
            db=db,
            skip=skip,
            limit=limit,
            isActive=isActive,
            status=status,
            search=search
        )
        
        # Convert to response DTOs
        return [CrudExampleResponse.model_validate(example) for example in crud_examples]

    async def get_crud_example_detail(
        self,
        db: Session,
        example_id: int
    ) -> CrudExampleResponse:
        """
        Get a single crud example by ID
        """
        crud_example = self.crud_example_repository.get_by_id(
            db=db,
            id=example_id
        )
        if not crud_example:
            logger.warning(f"Crud example not found: id={example_id}")
            return None
        return CrudExampleResponse.model_validate(crud_example)
    
    async def create_crud_example(
        self,
        db: Session,
        crud_example_data: CrudExampleCreate
    ) -> CrudExampleResponse:
        """
        Create a new crud example
        """
        logger.info(f"Creating new crud example: {crud_example_data.name}")

        # Validate business rules (if any)
        self._validate_crud_example_creation(crud_example_data)

        # Use repository to create crud example
        crud_example = self.crud_example_repository.create_crud_example(db, crud_example_data)

        logger.info(f"Successfully created crud example with ID: {crud_example.id}")
        return CrudExampleResponse.model_validate(crud_example)

    async def update_crud_example(
        self,
        db: Session,
        example_id: int,
        crud_example_update: CrudExampleUpdate
    ) -> Optional[CrudExampleResponse]:
        """
        Update an existing crud example
        """
        logger.info(f"Updating crud example ID: {example_id} with data: {crud_example_update}")

        # Validate business rules (if any)
        self._validate_crud_example_update(crud_example_update)

        # Use repository to update crud example
        updated_crud_example = self.crud_example_repository.update_crud_example(
            db=db,
            crud_example_id=example_id,
            crud_example_update=crud_example_update
        )

        if not updated_crud_example:
            logger.warning(f"Crud example not found for update: id={example_id}")
            return None

        logger.info(f"Successfully updated crud example with ID: {example_id}")
        return CrudExampleResponse.model_validate(updated_crud_example)

    async def delete_crud_example(
        self,
        db: Session,
        example_id: int
    ) -> bool:
        """
        Delete a crud example by ID
        """
        logger.info(f"Deleting crud example with ID: {example_id}")

        success = self.crud_example_repository.delete_crud_example_by_id(
            db=db,
            crud_example_id=example_id
        )

        if success:
            logger.info(f"Successfully deleted crud example with ID: {example_id}")
        else:
            logger.warning(f"Crud example not found for deletion: id={example_id}")

        return success

    def _validate_crud_example_creation(self, crud_example_data: CrudExampleCreate) -> None:
        """
        Validate business rules for crud example creation
        """
        # Example business rules:
        # - Name cannot be empty (already handled by Pydantic)
        # - Name cannot be too long
        # - Description cannot contain inappropriate content

        if len(crud_example_data.name.strip()) == 0:
            raise ValueError("Crud example name cannot be empty")

        if len(crud_example_data.name) > 200:
            raise ValueError("Crud example name is too long")

        # Add more business validation as needed
        logger.debug("Crud example creation validation passed")

    def _validate_crud_example_update(self, crud_example_update: CrudExampleUpdate) -> None:
        """
        Validate business rules for crud example updates
        """
        if crud_example_update.name is not None:
            if len(crud_example_update.name.strip()) == 0:
                raise ValueError("Crud example name cannot be empty")

            if len(crud_example_update.name) > 200:
                raise ValueError("Crud example name is too long")

        logger.debug("Crud example update validation passed")