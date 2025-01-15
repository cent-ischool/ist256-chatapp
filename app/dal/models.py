from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List
from sqlmodel import Field, SQLModel

class AuthModel(BaseModel):
    session_id: str = ""
    email: str = ""
    name: str = ""
    firstname: str = ""
    auth_data: dict = {}

    @staticmethod
    def from_auth_data(auth_data: dict):
        return AuthModel(
            session_id=auth_data["account"]["localAccountId"],
            email=auth_data['account']["idTokenClaims"]["preferred_username"],
            name=auth_data['account']["idTokenClaims"]["name"],
            firstname = auth_data['account']["idTokenClaims"]["name"].split(" ")[0],
            auth_data=auth_data
        )

class LogModel(SQLModel, table=True):
    __tablename__ = "logs"
    id: Optional[int] = Field(default=None, primary_key=True)
    sessionid: str
    userid: str
    timestamp: str
    model: str
    rag: bool
    context: str
    role: str
    content: str
