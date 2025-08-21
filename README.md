### ▶️ n8n-bot — Инструкция по установке и запуску


##### Цикл 1
Удаление старых артефактов, скачивание актуального проекта с github, сборка образа и запуск контейнера:
```bash
docker rm n8n-bot -f && docker rmi n8n-bot:latest -f && git pull && docker build --network=host -t n8n-bot:latest . && docker run -d --name n8n-bot -v ~/n8n_study_bot/images:/bot/images --restart=unless-stopped n8n-bot:latest
```


#### Сборка образа

##### Стандартная сборка
```bash
docker build -t n8n-bot:latest .
```

##### Сборка с доступом к хостовой сети (для сложных сетевых условий)
```bash
docker build --network=host -t n8n-bot:latest .
```
##### Сборка образа удаленно с GitHub репозитория
```bash
docker build -t n8n-bot https://github.com/AlexandrSilich/n8n_bot_study.git###main
```

#### Запуск контейнера

##### Первый запуск в фоне с назначением имени контейнеру
```bash
docker run -d --name n8n-bot -v ~/n8n_study_bot/images:/bot/images --restart=unless-stopped n8n-bot:latest
```
##### Повторные запуски
```bash
docker start n8n-bot

```
docker start всегда запускает в фоне
docker run vs docker start
  
docker run - создает НОВЫЙ контейнер

#### Управление контейнерами

##### Просмотр логов контейнера
```bash
docker logs n8n-bot
```
##### Остановка контейнера
```bash
docker stop n8n-bot
```
##### Удаление контейнера
```bash
docker rm n8n-bot -f
```
##### Удаление образа
```bash
docker rmi n8n-bot:latest -f
```

#### 📝 Дополнительные полезные команды

##### Просмотр использования места Docker
```bash
docker system df
```

##### Очистка неиспользуемых ресурсов
```bash
docker system prune
```

##### Запуск контейнера с интерактивным режимом для отладки
```bash
docker run -it --name n8n-bot-debug n8n-bot:latest /bin/bash
```

#### ▶️ Git комманды

Если рассинхрон версий файлов на сервере линукс и github, тогда принудительно счиатаем, что главная версия проекта на github
```bash
git reset --hard
```

#### ⚠️ Решение проблем

Проблемы с сетевым доступом при сборке
Чтобы не зависеть от флага --network=host в будущем и сделать решение постоянным:

🔧 Настройка DNS для демона Docker

Создать/отредактировать файл конфигурации:

```bash
sudo nano /etc/docker/daemon.json
```
Добавить DNS серверы:

```json
{
  "dns": ["1.1.1.1", "8.8.8.8"]
}
```
Перезапустить Docker:

```bash
sudo systemctl restart docker
```
Теперь можно собирать без host-сети:

```bash
docker build -t n8n-bot:latest .
```
