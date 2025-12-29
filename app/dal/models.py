from datetime import datetime
from loguru import logger
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


class AppSettingsModel(BaseModel):
    """Application settings model - stores AI config and system prompts."""
    ai_model: str = "gpt-4o-mini"
    temperature: float = 0.0
    answer_prompt: str = "Your name is Answerbot. You're have knowledge of Python programming."
    tutor_prompt: str = "Your name is Tutorbot. You're a supportive AI Python programming tutor."
    whitelist: str = ""

    @staticmethod
    def from_yaml_string(yaml_string: str) -> "AppSettingsModel":
        """Load settings gracefully, using defaults for missing fields."""
        try:
            data = yaml.safe_load(yaml_string) or {}
            config = data.get('configuration', {})
            return AppSettingsModel(
                ai_model=config.get('ai_model', 'gpt-4o-mini'),
                temperature=config.get('temperature', 0.0),
                answer_prompt=config.get('answer_prompt', "Your name is Answerbot. You're have knowledge of Python programming."),
                tutor_prompt=config.get('tutor_prompt', "Your name is Tutorbot. You're a supportive AI Python programming tutor."),
                whitelist=config.get('whitelist', '')
            )
        except Exception as e:
            logger.error(f"Error loading AppSettingsModel from YAML: {e}")
            return AppSettingsModel()  # Return model with all defaults

    def to_yaml_string(self) -> str:
        data = {
            'configuration': {
                'ai_model': self.ai_model,
                'temperature': self.temperature,
                'answer_prompt': self.answer_prompt,
                'tutor_prompt': self.tutor_prompt,
                'whitelist': self.whitelist
            }
        }
        return yaml.dump(data)


# Backwards compatibility alias (deprecated)
ConfigurationModel = AppSettingsModel

# Let's fold up the session state into a single Object    
# class SessionStateModel(BaseModel):
#     sessionid: str = Field(primary_key=True)
#     userid: str
#     mode: str = "Tutor"
#     context: str = "General Python"
#     last_updated: datetime = Field(default_factory=datetime.utcnow)

# User Preferences Model - loaded and saved whenever the user changes mode/context
class UserPreferencesModel(SQLModel, table=True):
    __tablename__ = "user_preferences"
    user_email: str = Field(default=None, primary_key=True)
    mode: str = "Tutor"
    context : str = "General Python"


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

