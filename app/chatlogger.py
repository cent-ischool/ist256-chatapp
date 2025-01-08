from datetime import datetime, timezone
from dal.models import LogModel

class ChatLogger:

    def __init__(self, db):
        self.__db = db

    def log(self, sessionid, userid, timestamp, role, content):
        lm = LogModel(
            sessionid=sessionid,
            userid=userid,
            timestamp=timestamp,
            role=role,
            content=content
        )                         
        with self.__db.get_session() as session:
            session.add(lm)
            result = session.commit()
        return result
    
    def log_user_prompt(self, sessionid, userid, prompt):
        return self.log(sessionid, userid, timestamp(), "user", prompt)
       
    def log_assistant_response(self, sessionid, userid, response):
        return self.log(sessionid, userid, timestamp(), "assistant", response)
    
    def log_system_prompt(self, appid, userid, system_prompt):
        return self.log(appid, userid, timestamp(), "system", system_prompt)

def timestamp(as_int=False):
    if not as_int:
        return datetime.now(timezone.utc).isoformat()
    else:
        return int(datetime.now(timezone.utc).timestamp())



    
