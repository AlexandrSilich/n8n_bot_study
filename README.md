🤖 n8n-bot — Инструкция по установке и запуску

Сборка образа

# Стандартная сборка
docker build -t n8n-bot:latest .

# Сборка с доступом к хостовой сети (для сложных сетевых условий)
docker build --network=host -t n8n-bot:latest .

# Сборка образа удаленно с GitHub репозитория
docker build -t n8n-bot https://github.com/AlexandrSilich/n8n_bot_study.git#main



Запуск контейнера

# Первый запуск в фоне с назначением имени контейнеру
docker run -d --name n8n-bot n8n-bot:latest

# Повторные запуски в фоне
docker run -d n8n-bot:latest



Управление контейнерами

# Просмотр логов контейнера
docker logs n8n-bot

# Остановка контейнера
docker stop n8n-bot

# Удаление контейнера
docker rm n8n-bot

# Удаление образа
docker rmi n8n-bot:latest



📝 Дополнительные полезные команды

# Просмотр использования места Docker
docker system df

# Очистка неиспользуемых ресурсов
docker system prune

# Запуск контейнера с интерактивным режимом для отладки
docker run -it --name n8n-bot-debug n8n-bot:latest /bin/bash


# ⚠️ Решение проблем

Проблемы с сетевым доступом при сборке
Чтобы не зависеть от флага --network=host в будущем и сделать решение постоянным:

🔧 Настройка DNS для демона Docker
Создать/отредактировать файл конфигурации:

bash
sudo nano /etc/docker/daemon.json
Добавить DNS серверы:

json
{
  "dns": ["1.1.1.1", "8.8.8.8"]
}
Перезапустить Docker:

bash
sudo systemctl restart docker
Теперь можно собирать без host-сети:

bash
docker build -t n8n-bot:latest .
