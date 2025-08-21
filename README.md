# n8n-bot — Инструкция по установке и запуску


## ▶️ 2. docker комманды

Просмотр запущенных контейнеров
docker ps

Просмотр всех контейнеров
docker ps -a

Сборка с доступом к хостовой сети (для сложных сетевых условий)
docker build --network=host -t n8n-bot:latest .

Первый запуск в фоне  (назначаем имя контейнеру)
docker run -d --name n8n-bot n8n-bot:latest

Повторные запуски в фоне
docker run -d n8n-bot:latest

Просмотр логов контейнера
docker logs n8n-bot

Остановка контейнера
docker stop n8n-bot

Удаление контейнера
docker rm n8n-bot

Удаление образа
docker rmi n8n-bot:latest

Сборка образа удаленно с репозитория
docker build -t n8n-bot https://github.com/AlexandrSilich/n8n_bot_study.git#main

 3. Запуск контейнера

## ▶️ 2. Git комманды

Если рассинхрон версий файлов на сервере линукс и github, тогда принудительно счиатаем, что главная версия проекта на github
```bash
git reset --hard



## ⚠️ 3. Проблемы

Чтобы не зависеть от флага --network=host в будущем и сделать решение постоянным, есть несколько вариантов.

Как закрепить решение
Настроить DNS для демона Docker:

Создать/отредактировать /etc/docker/daemon.json:
{
"dns": ["1.1.1.1","8.8.8.8"]
}

Перезапустить Docker:

sudo systemctl restart docker

Собирать без host-сети:

docker build -t n8n-bot:latest .
