import re
from datetime import datetime
from typing import Dict, Any

def sanitize_input(text: str) -> str:
    """清理用户输入"""
    if not text:
        return ""
    
    # 移除多余的空白字符
    text = re.sub(r'\s+', ' ', text.strip())
    
    # 限制长度
    if len(text) > 2000:
        text = text[:2000]
    
    return text

def format_response(success: bool, data: Any = None, error: str = None) -> Dict:
    """统一格式化API响应"""
    response = {
        'success': success,
        'timestamp': datetime.now().isoformat()
    }
    
    if success and data is not None:
        response['data'] = data
    
    if not success and error:
        response['error'] = error
    
    return response

def validate_session_id(session_id: str) -> bool:
    """验证session_id格式"""
    if not session_id:
        return False
    
    # UUID格式验证
    uuid_pattern = r'^[0-9a-f{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
    return bool(re.match(uuid_pattern, session_id, re.IGNORECASE))