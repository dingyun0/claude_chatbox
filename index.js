class ClaudeChatbot {
    constructor(apiUrl = 'http://localhost:5000/api') {
        this.apiUrl = apiUrl;
        this.sessionId = null;
    }
    
    async createSession() {
        const response = await fetch(`${this.apiUrl}/sessions`, {
            method: 'POST'
        });
        const data = await response.json();
        this.sessionId = data.session_id;
        return this.sessionId;
    }
    
    async sendMessage(message) {
        
        const response = await fetch(`${this.apiUrl}/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                messages: message,
                max_tokens: 100,
                temperature: 0.5,
                session_id: this.sessionId
            })
        });
        
        return await response.json();
    }
    
    async getHistory() {
        if (!this.sessionId) return null;
        
        const response = await fetch(`${this.apiUrl}/sessions/${this.sessionId}/history`);
        return await response.json();
    }
}

// 使用示例
const chatbot = new ClaudeChatbot();
chatbot.createSession().then(sessionId => {
    console.log('会话创建成功:', sessionId);
    
    chatbot.sendMessage('给我一首关于水的诗，用中文输出').then(response => {
        console.log('Claude回复:', response);
    });
});