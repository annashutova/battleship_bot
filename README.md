## ТЗ
Морской бот с ИИ
   - пользователь нужен только для отслеживания статуса игры
   - можно посмотреть статусы игр
   - сама игра:
     - реализации морского боя на питоне можно взять из интернета
     - при вводе пользователь отправляет клетку, которую собирается атаковать. Тут важна обработка ошибок
     - если успешно, в ответ бот присылает текущий бот пользователя + следующий от бота. С ходом бота
     - Саму отрисовку поля боя можно сделать с помощью символов массива.

# Инструкция по запуску проекта:
1. Перед запуском необходимо поднять проект [battleship_backend](https://github.com/annashutova/battleship_backend);
2. `git clone https://github.com/annashutova/battleship_bot` - Склонируйте репозиторий;
3. В папке `battleship_bot/conf` создайте файл `.env`;
```.env
BIND_IP=0.0.0.0
BIND_PORT=8005

METRICS_PORT=8005
BACKEND_HOST=http://web:8000

REDIS_PASSWORD=
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_DB=0

BOT_TOKEN=your_bot_token

#WEBHOOK_URL=your_webhook_url/tg

LOG_LEVEL=debug
```

Вместо `your_bot_token` необходимо вставить токен, полученный от бота [BotFather](https://t.me/BotFather)

## Запуск

- По умолчанию запуск производится через `polling`;
- Для запуска через `webhook` в .env файле необходимо раскомментировать WEBHOOK_URL и записать вместо `your_webhook_url` белый IP, настроенный на переадресацию `BIND_PORT`.

4. Находясь в папке `battleship_bot` поднимите докер:
```shell
docker compose up --build
``` 