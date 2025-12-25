"""
Base model with user tracking for FISY application.

Provides automatic tracking of user who created and last modified each record.
"""

from gws_core import CurrentUserService, Model
from peewee import ForeignKeyField

from gws_fisy.user.user import User

from .fisy_db_manager import FisyDbManager


class ModelWithUser(Model):
    """
    Base model with user tracking.

    Automatically tracks created_by and last_modified_by users.
    All FISY models should inherit from this class.
    """

    # Use ForeignKey to reference the local User entity
    created_by = ForeignKeyField(User, null=False, backref="+")
    last_modified_by = ForeignKeyField(User, null=False, backref="+")

    def _before_insert(self) -> None:
        """Set created_by and last_modified_by before insert."""
        super()._before_insert()
        current_user = CurrentUserService.get_and_check_current_user()
        self.created_by = current_user
        self.last_modified_by = current_user

    def _before_update(self) -> None:
        """Update last_modified_by before update."""
        super()._before_update()
        current_user = CurrentUserService.get_and_check_current_user()
        self.last_modified_by = current_user

    class Meta:
        database = FisyDbManager.get_instance().db
        db_manager = FisyDbManager.get_instance()
