from datetime import datetime, timezone
from dal.models import LogModel

class ChatLogger:

    def __init__(self, db, model:str, rag:bool):
        self.__db = db
        self.__model = model
        self.__rag = rag

    def log(self, sessionid, userid, timestamp, model, rag, context, role, content):
        lm = LogModel(
            sessionid=sessionid,
            userid=userid,
            model=model,
            rag=rag,
            context=context,
            timestamp=timestamp,
            role=role,
            content=content
        )                         
        with self.__db.get_session() as session:
            session.add(lm)
            result = session.commit()
        return result
    
    def log_user_prompt(self, sessionid, userid, context, prompt):
        return self.log(sessionid, userid, timestamp(), self.__model, self.__rag, context, "user", prompt)
       
    def log_assistant_response(self, sessionid, userid, context, response):
        return self.log(sessionid, userid, timestamp(), self.__model, self.__rag, context, "assistant", response)
    
    def log_system_prompt(self, appid, userid, system_prompt):
        return self.log(appid, userid, timestamp(), self.__model, self.__rag, "N/A", "system", system_prompt)

def timestamp(as_int=False):
    if not as_int:
        return datetime.now(timezone.utc).isoformat()
    else:
        return int(datetime.now(timezone.utc).timestamp())



    
