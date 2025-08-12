from fastapi import FastAPI, Request
import os
import json

app = FastAPI()

@app.get("/")
def root():
    """Проверка работы"""
    return {
        "message": "ADHD Bot is alive!",
        "status": "working",
        "token_exists": bool(os.getenv("BOT_TOKEN"))
    }

@app.post("/")
async def webhook(request: Request):
    """Простой webhook handler"""
    try:
        # Получаем данные
        body = await request.body()
        data = json.loads(body.decode('utf-8'))
        
        # Логируем что получили
        print(f"Received: {data}")
        
        # Простая обработка
        if 'message' in data:
            message = data['message']
            if 'text' in message:
                text = message['text']
                chat_id = message['chat']['id']
                
                print(f"Message: {text} from chat: {chat_id}")
                
                # Пока просто логируем, без отправки ответа
                if text == '/start':
                    print("Start command received")
                
        return {"ok": True, "status": "received"}
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return {"ok": False, "error": str(e)}