#!/bin/sh
set -e

echo "Waiting for RabbitMQ to be ready..."

# Ожидаем доступности RabbitMQ
while ! nc -z $RABBITMQ_HOST $RABBITMQ_PORT; do
  sleep 1
done

echo "RabbitMQ is ready! Setting up admin data..."

# Устанавливаем rabbitmqadmin если нет
if ! command -v rabbitmqadmin >/dev/null; then
  echo "Installing rabbitmqadmin..."
  wget -q http://rabbitmq:15672/cli/rabbitmqadmin -O /usr/local/bin/rabbitmqadmin
  chmod +x /usr/local/bin/rabbitmqadmin
fi

# Создаем очередь для хранения админов
rabbitmqadmin -H $RABBITMQ_HOST -u $RABBITMQ_USER -p $RABBITMQ_PASSWORD declare queue name=telegram_admins durable=true

# Добавляем администратора
rabbitmqadmin -H $RABBITMQ_HOST -u $RABBITMQ_USER -p $RABBITMQ_PASSWORD publish \
  exchange=amq.default \
  routing_key=telegram_admins \
  payload="{\"name\":\"$ADMIN\",\"role\":\"ADMIN\"}" \
  properties='{"delivery_mode":2}'

echo "Admin $ADMIN successfully added to RabbitMQ"