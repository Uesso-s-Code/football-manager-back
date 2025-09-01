from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from passlib.context import CryptContext

# Para evitar erro de forward reference
if TYPE_CHECKING:
    from models import Role, Team

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    email: str
    hashed_password: str
    rolefk: Optional[int] = Field(default=None, foreign_key="role.id")
    role: Optional["Role"] = Relationship(back_populates="users")
    teamfk: Optional[int] = Field(default=None, foreign_key="team.id")
    team: Optional["Team"] = Relationship(back_populates="users")
    is_active: bool = True

    def verify_password(self, password: str) -> bool:
        return pwd_context.verify(password, self.hashed_password)


class Role(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str

    # Relacionamento inverso com User
    users: List["User"] = Relationship(back_populates="role")


class Team(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    league: Optional[str] = None
    founded: Optional[int] = None
    stadium: Optional[str] = None
    manager: Optional[str] = None

    # Relacionamento com usuários
    users: List["User"] = Relationship(back_populates="team")

    # Campos adicionais calculados
    users_count: int = Field(default=0, sa_column_kwargs={"default": 0, "server_default": "0"})
    users_active_count: int = Field(default=0, sa_column_kwargs={"default": 0, "server_default": "0"})
    users_inactive_count: int = Field(default=0, sa_column_kwargs={"default": 0, "server_default": "0"})
