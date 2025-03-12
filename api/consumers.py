import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from rest_framework.authtoken.models import Token
from .ai_model import dream_generator
from .models import Dream

class DreamConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Extract token from query string
        query_string = self.scope["query_string"].decode()
        token_key = None
        for param in query_string.split("&"):
            if param.startswith("token="):
                token_key = param.split("=")[1]

        if not token_key:
            await self.close()
            return

        # Authenticate user with token
        user = await self.get_user_from_token(token_key)
        if not user or user.is_anonymous:
            await self.close()
            return

        self.scope["user"] = user
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        data = json.loads(text_data)
        prompt = data.get("prompt")
        output = dream_generator.generate_dream(prompt)
        
        await database_sync_to_async(self.save_dream)(prompt, output)
        await self.send(text_data=json.dumps({"dream": output}))

    @database_sync_to_async
    def get_user_from_token(self, token_key):
        try:
            token = Token.objects.get(key=token_key)
            return token.user
        except Token.DoesNotExist:
            return None

    @database_sync_to_async
    def save_dream(self, prompt, output):
        Dream.objects.create(user=self.scope["user"], prompt=prompt, output=output)