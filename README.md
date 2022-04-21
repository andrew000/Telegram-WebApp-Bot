# Simple Telegram Web App Bot

***

1. Clone repo.
2. Edit `.env-example` file, rename it to `.env`, paste BOT_TOKEN from https://t.me/botfather and paste ENDPOINT (your
   SERVER DOMAIN to accept requests).
3. Setup server to accept requests on port `45678` (You can change port in `docker-compose.yml` and `main.py:84`).
4. Now you can: start `main.py` manually (not recommended) OR use `deploy.sh` to start `Bot` in `Docker` (recommended)
5. Finally, go to bot PM and use `/start`