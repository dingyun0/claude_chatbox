from flask import Blueprint, request, jsonify
from api.services import ChatService
import uuid

api_bp = Blueprint('api', __name__)
claude_service = ChatService()

@api_bp.route('/chat', methods=['POST'])
def chat():
    """聊天接口"""
    try:
        data = request.get_json()
        if not data or 'messages' not in data:
            return jsonify({
                'success': False,
                'error': 'Message is required'
            }), 400
        
        user_message = data['messages']
        session_id = data.get('session_id', str(uuid.uuid4()))
        # 调用Claude服务
        result = claude_service.chat_with_claude(session_id, user_message)
        
        if result['success']:
            return jsonify(result)
        else:
            return jsonify(result), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@api_bp.route('/sessions/<session_id>/history', methods=['GET'])
def get_session_history(session_id):
    """获取会话历史"""
    result = claude_service.get_session_history(session_id)
    
    if result['success']:
        return jsonify(result)
    else:
        return jsonify(result), 404

@api_bp.route('/sessions/<session_id>/clear', methods=['DELETE'])
def clear_session(session_id):
    """清除会话"""
    result = claude_service.clear_session(session_id)
    
    if result['success']:
        return jsonify(result)
    else:
        return jsonify(result), 404

@api_bp.route('/sessions', methods=['POST'])
def create_session():
    """创建新会话"""
    session_id = str(uuid.uuid4())
    return jsonify({
        'success': True,
        'session_id': session_id,
        'message': 'New session created'
    })