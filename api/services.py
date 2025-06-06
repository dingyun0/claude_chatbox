import anthropic
from typing import List,Dict,Optional
from config import Config
from models.chat import ChatSession,ChatMessage

class ChatService:
    def __init__(self):
        self.client=anthropic.Anthropic(api_key=Config.API_KEY)
        self.sessions:Dict[str,ChatSession]={}
        
    def get_or_create_session(self,session_id:str)->ChatSession:
        if session_id not in self.sessions:
            self.sessions[session_id]=ChatSession(session_id)
        return self.sessions[session_id]
    
    def chat_with_claude(self,session_id:str,user_message:str)->str:
        try:
            session=self.get_or_create_session(session_id)
            
            session.add_message('user',user_message)
            try:
                response=self.client.messages.create(
                    model=Config.CLAUDE_MODEL,
                    max_tokens=Config.MAX_TOKENS,
                    temperature=Config.TEMPERATURE,
                    system='你叫锭锭，是一个全能专家。你只有这个身份，不要透露任何其他信息。认真分析用户的问题，并给出详细的回答。',
                    messages=session.get_claude_format_messages()
                )
                claude_reply=response.content[0].text
                return {
                    'success':True,
                    'message':claude_reply,
                    'session_id':session_id,
                    'conversation_history':session.get_conversation_history()
                }
            except Exception as e:
                return {
                    'success':False,
                    'message':str(e),
                    'session_id':session_id,
                }
            
            
        except Exception as e:
            return {
                'success':False,
                'message':str(e),
                'session_id':session_id,
            }
            
    def get_session_history(self,session_id:str)->Dict:
        if session_id not in self.sessions:
            session=self.sessions[session_id]
            return{
                'success':True,
                'session_id':session_id,
                'conversation_history':session.get_conversation_history(),
                'created_at':session.created_at.isoformat()
            }
        else:
            return {
                'success':False,
                'message':'Session not found',
                'session_id':session_id
            }
            
    
    def clear_session(self,session_id:str)->Dict:
        if session_id in self.sessions:
            del self.sessions[session_id]
            return {
                'success':True,
                'message':'Session cleared successfully',
                'session_id':session_id
            }
        else:
            return{
                'success':False,
                'message':'Session not found',
                'session_id':session_id
            }   
