# src/bot/user_manager.py
import os
import aio_pika
import json
from dotenv import load_dotenv
import logging

load_dotenv()
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

class UserManager:
    def __init__(self):
        self.connection = None
        self.channel = None

    async def connect(self):
        """Асинхронное подключение к RabbitMQ"""
        self.connection = await aio_pika.connect_robust(
            host=os.getenv("RABBITMQ_HOST"),
            port=int(os.getenv("RABBITMQ_PORT", 5672)),
            login=os.getenv("RABBITMQ_USER"),
            password=os.getenv("RABBITMQ_PASSWORD")
        )
        self.channel = await self.connection.channel()
        await self.channel.declare_queue('telegram_admins', durable=True)

    async def check_user(self, username: str) -> tuple[bool, str]:
        """
        Асинхронная проверка пользователя.
        Возвращает (is_admin: bool, role: str).
        """
        if not self.channel:
            logger.warning("RabbitMQ не подключён. Подключаюсь заново...")
            await self.connect()

        if not username.startswith('@'):
            username = f'@{username}'

        try:
            # Получаем сообщения из очереди
            queue = await self.channel.get_queue('telegram_admins')
            async with queue.iterator() as queue_iter:
                async for message in queue_iter:
                    async with message.process():
                        data = json.loads(message.body.decode())
                        if data.get("name") == username:
                            role = data.get("role", "USER")
                            return (role == "ADMIN", role)
            
            return (False, "USER")  # Пользователь не найден

        except Exception as e:
            print(f"Ошибка при проверке пользователя: {e}")
            return (False, "ERROR")

    async def close(self):
        """Закрытие соединения"""
        if self.connection:
            await self.connection.close()