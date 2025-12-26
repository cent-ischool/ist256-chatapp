from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List
from sqlmodel import Field, SQLModel
import yaml

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


class ConfigurationModel(BaseModel):
    ai_model: str
    system_prompt: str
    temperature: float
    whitelist: str
    system_prompt_text: Optional[str] = None


    @staticmethod
    def from_yaml_string(yaml_string: str):
        data = yaml.safe_load(yaml_string)
        config = data.get('configuration', {})
        model =  ConfigurationModel(
            ai_model=config.get('ai_model', 'gpt-5-nano'),
            system_prompt=config.get('system_prompt', 'original'),
            temperature=config.get('temperature', 0.0),
            whitelist=config.get('whitelist', 'roster.txt')
        )
        return model

    def to_yaml_string(self) -> str:
        data = {
            'configuration': {
                'ai_model': self.ai_model,
                'system_prompt': self.system_prompt,
                'temperature': self.temperature,
                'whitelist': self.whitelist
            }
        }
        return yaml.dump(data)

# Database Models
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

