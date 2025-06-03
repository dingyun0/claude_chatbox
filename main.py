from flask import Flask, render_template_string
from flask_cors import CORS
from config import Config
from api.routes import api_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # 启用CORS
    CORS(app)
    
    # 注册蓝图
    app.register_blueprint(api_bp, url_prefix='/api')
    
    # 根路径
    @app.route('/')
    def index():
        return render_template_string('''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Claude Chatbot API</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; }
                .container { max-width: 800px; margin: 0 auto; }
                .endpoint { background: #f5f5f5; padding: 15px; margin: 10px 0; border-radius: 5px; }
                code { background: #e8e8e8; padding: 2px 4px; border-radius: 3px; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Claude Chatbot API</h1>
                <p>欢迎使用Claude对话机器人API！</p>
                
                <h2>API接口文档</h2>
                
                <div class="endpoint">
                    <h3>POST /api/chat</h3>
                    <p>发送消息给Claude</p>
                    <p><strong>请求体:</strong></p>
                    <pre><code>{
    "message": "你好，Claude！",
    "session_id": "可选的会话ID"
}</code></pre>
                </div>
                
                <div class="endpoint">
                    <h3>GET /api/sessions/&lt;session_id&gt;/history</h3>
                    <p>获取会话历史记录</p>
                </div>
                
                <div class="endpoint">
                    <h3>DELETE /api/sessions/&lt;session_id&gt;/clear</h3>
                    <p>清除会话记录</p>
                </div>
                
                <div class="endpoint">
                    <h3>POST /api/sessions</h3>
                    <p>创建新的会话</p>
                </div>
                
                <h2>使用说明</h2>
                <ol>
                    <li>获取Claude API密钥并配置到.env文件中</li>
                    <li>使用POST请求发送消息到/api/chat</li>
                    <li>系统会自动管理会话状态</li>
                    <li>可以通过session_id获取历史对话</li>
                </ol>
            </div>
        </body>
        </html>
        ''')
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(
        host='0.0.0.0',
        port=Config.PORT,
        debug=Config.DEBUG
    )