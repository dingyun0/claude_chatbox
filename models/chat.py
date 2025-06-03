from datetime import datetime
from typing import List,Dict,Optional

class ChatMessage:
    def __init__(self,role:str,content:str,timestamp:Optional[datetime] = None):
        self.role=role
        self.content=content
        self.timestamp=timestamp
        
    def to_dict(self)->Dict:
        return{
            'role':self.role,
            'content':self.content
        }

class ChatSession:
    def __init__(self,session_id:str):
        self.session_id=session_id
        self.messages:List[ChatMessage]=[]
        self.created_at=datetime.now()
        
    def add_message(self,role:str,content:str):
        message=ChatMessage(role,content)
        self.messages.append(message)
        return message 
    
    def get_conversation_history(self)->List[Dict]:
        return [msg.to_dict() for msg in self.messages]
    
    """转换为Claude API需要的格式"""
    def get_claude_format_messages(self)->List[Dict]:
        return [{'role':msg.role,'content':msg.content} for msg in self.messages]
