# Bot-for-pull-request 🤖🔔

**Telegram-бот для разработчиков**, который следит за Pull Request'ами на GitHub и уведомляет о любых изменениях. Идеален для тех, кто хочет оперативно получать обновления, не заходя на GitHub.

## 📌 Возможности

- 🔗 Подключение к вашему GitHub аккаунту через токен
- 📂 Отслеживание Pull Request'ов в выбранных репозиториях
- 🔄 Проверка на наличие:
  - новых PR
  - обновлений в существующих PR
  - закрытых и смерженных PR
- 📬 Уведомления в Telegram с краткой сводкой:
  - Название PR
  - Автор
  - Текущий статус (open/closed/merged)
  - Прямая ссылка на PR

## 💬 Управление ботом

Управление осуществляется через удобные **inline-кнопки** и минимальное количество команд.

## 🧰 Установка и запуск

1. **Клонируйте репозиторий и установите зависимости:**

```bash
git clone https://github.com/yourusername/Bot-for-pull-request.git
cd Bot-for-pull-request
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. **Создайте в корне проекта файл `.env` со следующим содержимым:**
```env
TELEGRAM_TOKEN=token
RABBITMQ_HOST=host_rabbitmq
RABBITMQ_PORT=port_rabbitmq
RABBITMQ_USER=user_rabbitmq
RABBITMQ_PASSWORD=pass_rabbitmq
ADMIN=@username
```

3. **Запустите бота командой**
```bash
python bot.py
```

## 🐳 Запуск через Docker Compose

Если у вас уже есть готовый файл `docker-compose.yml`, просто выполните команду:

```bash
docker compose up -d --build
```

Контейнер запустится в фоне с настройками из `docker-compose.yml`.
Убедитесь, что файл .env с переменными окружения находится в той же папке, или переменные переданы в docker-compose.yml.