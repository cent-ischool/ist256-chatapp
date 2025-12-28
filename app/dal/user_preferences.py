from typing import Optional
from loguru import logger
from sqlmodel import select
from dal.db import PostgresDb
from dal.models import UserPreferencesModel


def get_preferences(db: PostgresDb, user_email: str) -> Optional[UserPreferencesModel]:
    """
    Retrieve user preferences from database.

    Args:
        db: PostgresDb instance
        user_email: User's email address (primary key)

    Returns:
        UserPreferencesModel if found, None if not found or error occurs
    """
    try:
        with db.get_session() as session:
            statement = select(UserPreferencesModel).where(
                UserPreferencesModel.user_email == user_email
            )
            preferences = session.exec(statement).first()

            if preferences:
                logger.info(f"Loaded preferences: email={user_email}, mode={preferences.mode}, context={preferences.context}")
            else:
                logger.info(f"No preferences found for: email={user_email}")

            return preferences

    except Exception as e:
        logger.error(f"Error loading preferences: email={user_email}, error={e}")
        return None


def save_preferences(db: PostgresDb, user_email: str, mode: str, context: str) -> UserPreferencesModel:
    """
    Save or update user preferences in database.

    Args:
        db: PostgresDb instance
        user_email: User's email address (primary key)
        mode: AI mode ("Tutor" or "Answer")
        context: Chat context (assignment name or "General Python")

    Returns:
        Saved UserPreferencesModel

    Raises:
        Exception if database operation fails
    """
    try:
        with db.get_session() as session:
            # Check if preferences exist
            statement = select(UserPreferencesModel).where(
                UserPreferencesModel.user_email == user_email
            )
            existing = session.exec(statement).first()

            if existing:
                # Update existing preferences
                existing.mode = mode
                existing.context = context
                session.add(existing)
                session.commit()
                session.refresh(existing)
                logger.info(f"Updated preferences: email={user_email}, mode={mode}, context={context}")
                return existing
            else:
                # Create new preferences
                new_prefs = UserPreferencesModel(
                    user_email=user_email,
                    mode=mode,
                    context=context
                )
                session.add(new_prefs)
                session.commit()
                session.refresh(new_prefs)
                logger.info(f"Created preferences: email={user_email}, mode={mode}, context={context}")
                return new_prefs

    except Exception as e:
        logger.error(f"Error saving preferences: email={user_email}, mode={mode}, context={context}, error={e}")
        raise
