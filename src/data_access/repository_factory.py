from __future__ import annotations

from src.data_access.repositories.postgre import ClientRepo
from src.data_access.repositories.postgre import InteractionHistoryRepo
from src.data_access.repositories.postgre import ItemRepo
from src.data_access.repositories.postgre import OrderRepo
from src.data_access.repositories.postgre import UserRepo
from src.data_access.repositories_interface import IClientRepo
from src.data_access.repositories_interface import IInteractionHistoryRepo
from src.data_access.repositories_interface import IItemRepo
from src.data_access.repositories_interface import IOrderRepo
from src.data_access.repositories_interface import IUserRepo
from src.data_access.utils.db_connection_manager import db_manager


class RepositoryFactory:
    """Factory for creating repository instances with the shared database connection."""
    
    _user_repo: IUserRepo | None = None
    _client_repo: IClientRepo | None = None
    _order_repo: IOrderRepo | None = None
    _item_repo: IItemRepo | None = None
    _interaction_repo: IInteractionHistoryRepo | None = None
    _test_mode: bool = False
    _initialized: bool = False
    
    @classmethod
    async def initialize(cls, connection_string: str, test_mode: bool = False) -> None:
        cls._test_mode = test_mode
        cls._initialized = True
        cls._user_repo = None
        cls._client_repo = None
        cls._order_repo = None
        cls._item_repo = None
        cls._interaction_repo = None
    
        if not test_mode:
            await db_manager.initialize(connection_string)

    @classmethod
    def get_user_repo(cls) -> IUserRepo:
        """Get or create a UserRepo instance."""
        if cls._test_mode:
            if cls._user_repo is None:
                raise ValueError("Repository not set. In test mode, you must set repositories manually.")
            return cls._user_repo
    
        if cls._user_repo is None:
            if not db_manager.initialized:
                raise ValueError("Database connection not initialized. Call RepositoryFactory.initialize() first.")
            cls._user_repo = UserRepo(db_manager.get_pool())
        return cls._user_repo
    
    @classmethod
    def get_client_repo(cls) -> IClientRepo:
        """Get or create a ClientRepo instance."""
        if cls._test_mode:
            if cls._client_repo is None:
                raise ValueError("Repository not set. In test mode, you must set repositories manually.")
            return cls._client_repo
    
        if cls._client_repo is None:
            if not db_manager.initialized:
                raise ValueError("Database connection not initialized. Call RepositoryFactory.initialize() first.")
            cls._client_repo = ClientRepo(db_manager.get_pool())
        return cls._client_repo
    
    @classmethod
    def get_order_repo(cls) -> IOrderRepo:
        """Get or create an OrderRepo instance."""
        if cls._test_mode:
            if cls._order_repo is None:
                raise ValueError("Repository not set. In test mode, you must set repositories manually.")
            return cls._order_repo
    
        if cls._order_repo is None:
            if not db_manager.initialized:
                raise ValueError("Database connection not initialized. Call RepositoryFactory.initialize() first.")
            cls._order_repo = OrderRepo(db_manager.get_pool())
        return cls._order_repo

    @classmethod
    def get_item_repo(cls) -> IItemRepo:
        """Get or create an ItemRepo instance."""
        if cls._test_mode:
            if cls._item_repo is None:
                raise ValueError("Repository not set. In test mode, you must set repositories manually.")
            return cls._item_repo

        if cls._item_repo is None:
            if not db_manager.initialized:
                raise ValueError("Database connection not initialized. Call RepositoryFactory.initialize() first.")
            cls._item_repo = ItemRepo(db_manager.get_pool())
        return cls._item_repo

    @classmethod
    def get_interaction_repo(cls) -> IInteractionHistoryRepo:
        """Get or create an InteractionHistoryRepo instance."""
        if cls._test_mode:
            if cls._interaction_repo is None:
                raise ValueError("Repository not set. In test mode, you must set repositories manually.")
            return cls._interaction_repo

        if cls._interaction_repo is None:
            if not db_manager.initialized:
                raise ValueError("Database connection not initialized. Call RepositoryFactory.initialize() first.")
            cls._interaction_repo = InteractionHistoryRepo(db_manager.get_pool())
        return cls._interaction_repo

    @classmethod
    def set_user_repo(cls, repo: IUserRepo) -> None:
        """Set a custom user repository (for testing)."""
        cls._user_repo = repo

    @classmethod
    def set_client_repo(cls, repo: IClientRepo) -> None:
        """Set a custom client repository (for testing)."""
        cls._client_repo = repo

    @classmethod
    def set_order_repo(cls, repo: IOrderRepo) -> None:
        """Set a custom order repository (for testing)."""
        cls._order_repo = repo

    @classmethod
    def set_item_repo(cls, repo: IItemRepo) -> None:
        """Set a custom item repository (for testing)."""
        cls._item_repo = repo

    @classmethod
    def set_interaction_repo(cls, repo: IInteractionHistoryRepo) -> None:
        """Set a custom interaction repository (for testing)."""
        cls._interaction_repo = repo

    @classmethod
    async def close(cls) -> None:
        """Close the database connection manager."""
        if not cls._test_mode:
            await db_manager.close()

        # Clear repositories
        cls._user_repo = None
        cls._client_repo = None
        cls._order_repo = None
        cls._item_repo = None
        cls._interaction_repo = None
        cls._test_mode = False
