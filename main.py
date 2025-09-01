from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session, select
from database import engine, create_db
from auth import AuthJWT, register_auth_exception_handler
from models import User
from schemas import UserCreate, UserLogin, UserUpdate, UserRead
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

app = FastAPI(title="Football Manager API")
create_db()
register_auth_exception_handler(app)

def get_session():
    with Session(engine) as session:
        yield session

# --------------------------
# USERS
# --------------------------

@app.get("/users/{user_id}", response_model=UserRead)
def read_user(user_id: int, session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.id == user_id)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.post("/users/", response_model=UserRead)
def create_user(user: UserCreate, session: Session = Depends(get_session)):
    hashed_password = pwd_context.hash(user.password)
    db_user = User(
        name=user.username,
        email=user.email,
        hashed_password=hashed_password,
        rolefk=user.rolefk,
        teamfk=user.teamfk,
        is_active=user.is_active
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

@app.put("/users/{user_id}", response_model=UserRead)
def update_user(user_id: int, user_update: UserUpdate, session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.id == user_id)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user_update.password:
        user.hashed_password = pwd_context.hash(user_update.password)
    if user_update.username:
        user.name = user_update.username
    if user_update.email:
        user.email = user_update.email
    if user_update.rolefk is not None:
        user.rolefk = user_update.rolefk
    if user_update.teamfk is not None:
        user.teamfk = user_update.teamfk
    if user_update.is_active is not None:
        user.is_active = user_update.is_active

    session.add(user)
    session.commit()
    session.refresh(user)
    return user

# --------------------------
# LOGIN
# --------------------------

@app.post("/login")
def login(user_login: UserLogin, Authorize: AuthJWT = Depends(), session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.email == user_login.email)).first()
    if not user or not user.verify_password(user_login.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = Authorize.create_access_token(subject=str(user.id))
    return {"access_token": access_token, "token_type": "bearer"}

# --------------------------
# TEAM USERS
# --------------------------

@app.get("/teams/{team_id}/users", response_model=list[UserRead])
def get_team_users(team_id: int, Authorize: AuthJWT = Depends(), session: Session = Depends(get_session)):
    Authorize.jwt_required()
    users = session.exec(select(User).where(User.teamfk == team_id)).all()
    return users

# --------------------------
# HEALTH CHECK
# --------------------------

@app.get("/health")
def health_check():
    return {"status": "ok"}
