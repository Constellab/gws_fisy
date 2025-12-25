"""
Database manager for FISY application.

Provides backend features for managing the FISY database.
"""

from typing import Optional

from gws_core import LazyAbstractDbManager
from peewee import DatabaseProxy


class FisyDbManager(LazyAbstractDbManager):
    """
    DbManager class for FISY.

    Provides backend features for managing databases.
    """

    db = DatabaseProxy()

    _instance: Optional['FisyDbManager'] = None

    @classmethod
    def get_instance(cls) -> 'FisyDbManager':
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def get_name(self) -> str:
        return 'db'

    def get_brick_name(self) -> str:
        return 'gws_fisy'
