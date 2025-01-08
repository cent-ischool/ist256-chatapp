from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List

class AuthModel(BaseModel):
    session_id: str = ""
    email: str = ""
    name: str = ""
    auth_data: dict = {}

    @staticmethod
    def from_auth_data(auth_data: dict):
        return AuthModel(
            session_id=auth_data["account"]["localAccountId"],
            email=auth_data['account']["idTokenClaims"]["preferred_username"],
            name=auth_data['account']["idTokenClaims"]["name"],
            auth_data=auth_data
        )

