# This is a telegram bot to collect data of order in a chat room

## Requirement:
* pyTelegramBotAPI
* flask
* oauth2client
* gspread
* poetry

## Prepare!!!
* On telegram app, go to [botfather](https://telegram.me/BotFather) to make a telegram bot, then get API key and save into .env file
* Make google api: [The gspread documentation explains how to create Google OAuth2.0 JWTs](http://gspread.readthedocs.org/en/latest/oauth2.html)
* Save the JWTs file into working directory
* In the working directory, run `poetry install` to make the virtualenv. Then `poetry shell` to activate virtual environment, `poetry run python app.py` to run app in debug mode


## How to deploy?
- I use [render.com](https://dashboard.render.com/) to deploy this github project
- Click `New` button to deploy new project
- Choose `web service`
- Connect to github repo
- Remember to choose `Docker` to deploy.
- Click `Deploy` and cheers!
