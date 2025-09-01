from pydantic import BaseModel, EmailStr
from typing import Optional


# ---------------------
# USER SCHEMAS
# ---------------------

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    rolefk: Optional[int] = None
    teamfk: Optional[int] = None
    is_active: bool = True

class UserRead(BaseModel):
    id: int
    username: str
    email: EmailStr
    rolefk: Optional[int] = None
    teamfk: Optional[int] = None
    is_active: bool

    class Config:
        orm_mode = True

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    rolefk: Optional[int] = None
    teamfk: Optional[int] = None
    is_active: Optional[bool] = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


# ---------------------
# ROLE SCHEMAS
# ---------------------

class RoleCreate(BaseModel):
    name: str

class RoleRead(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


# ---------------------
# TEAM SCHEMAS
# ---------------------

class TeamCreate(BaseModel):
    name: str
    league: Optional[str] = None
    founded: Optional[int] = None
    stadium: Optional[str] = None
    manager: Optional[str] = None

class TeamRead(BaseModel):
    id: int
    name: str
    league: Optional[str] = None
    founded: Optional[int] = None
    stadium: Optional[str] = None
    manager: Optional[str] = None
    users_count: int = 0
    users_active_count: int = 0
    users_inactive_count: int = 0

    class Config:
        orm_mode = True

class TeamUpdate(BaseModel):
    name: Optional[str] = None
    league: Optional[str] = None
    founded: Optional[int] = None
    stadium: Optional[str] = None
    manager: Optional[str] = None
    users_count: Optional[int] = 0
    users_active_count: Optional[int] = 0
    users_inactive_count: Optional[int] = 0
