# Simple Telegram Web App Bot

***

1. Clone repo.
2. Edit `.env-example` file, rename it to `.env`, paste BOT_TOKEN from https://t.me/botfather and paste ENDPOINT (your
   SERVER DOMAIN to accept requests).
3. Setup server to accept requests on port `45678` (You can change port in `docker-compose.yml` and `main.py:84`).
4. Now you can: start `main.py` manually (not recommended) OR use `deploy.sh` to start `Bot` in `Docker` (recommended)
5. Finally, go to bot PM and use `/start`

***

# Problems
## WebApp doesn't work in web.telegram.org
:tipping_hand_man: If you use **WebApp** through the **web.telegram.org**, then **Nginx** will be very reluctant to give statics (**WILL NOT**).

:monocle_face: This is caused by the iframe security policy, which needs to be slightly adjusted in the **Nginx** settings.

:white_check_mark: I am attaching a solution to the problem in the screenshot. If you have security settings defined in **Nginx**, then look for such a setting in your configs and edit it as in my screenshot.

:warning: Don't forget to use `nginx -s reload` to update your config changes!

:sunglasses: As a result, **Nginx** will be happy to share static files with users of the **web.telegram.org**

![image](https://user-images.githubusercontent.com/11490628/164559948-5f52f36c-07d5-4b99-a0d0-b2af6621ae4d.png)

## White Screen in TDesktop
:tipping_hand_man: **TDesktop** on a **PC** does not know how to use **TLS 1.3**, so be sure to specify the ability to use **TLS 1.2** in the **Nginx** config.

**P.S.** :confused: _Now it seems too early for **TLS 1.3**_
