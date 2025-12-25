"""
User model for FISY application.

Local User entity stored in the FISY database, mirroring gws_core User.
"""

from gws_core import EnumField, Model, UserDTO, UserGroup
from gws_core import User as GwsCoreUser
from peewee import BooleanField, CharField

from ..core.fisy_db_manager import FisyDbManager


class User(Model):
    """Local User model for FISY database."""

    email: str = CharField()
    first_name: str = CharField()
    last_name: str = CharField()
    group: UserGroup = EnumField(choices=UserGroup, default=UserGroup.USER)
    is_active = BooleanField(default=True)
    photo: str = CharField(null=True)

    def to_dto(self) -> UserDTO:
        """Convert to UserDTO."""
        return UserDTO(
            id=self.id,
            email=self.email,
            first_name=self.first_name,
            last_name=self.last_name,
            photo=self.photo
        )

    @classmethod
    def from_gws_core_user(cls, gws_core_user: GwsCoreUser) -> "User":
        """Create or get a User instance from a gws_core User.

        :param gws_core_user: The gws_core User object
        :type gws_core_user: GwsCoreUser
        :return: The corresponding User instance
        :rtype: User
        """
        return User(
            id=gws_core_user.id,
            email=gws_core_user.email,
            first_name=gws_core_user.first_name,
            last_name=gws_core_user.last_name,
            group=gws_core_user.group,
            is_active=gws_core_user.is_active,
            photo=gws_core_user.photo,
            created_at=gws_core_user.created_at,
            last_modified_at=gws_core_user.last_modified_at,
        )

    class Meta:
        table_name = "gws_fisy_users"
        database = FisyDbManager.get_instance().db
        db_manager = FisyDbManager.get_instance()
        is_table = True
