# This is a telegram bot to collect data of order in a chat room

## Requirement:
* pyTelegramBotAPI
* flask
* oauth2client
* gspread
* pipenv

## Prepare!!!
* On telegram app, go to [botfather](https://telegram.me/BotFather) to make a telegram bot, then get API key and save into .env file
* Make google api: [The gspread documentation explains how to create Google OAuth2.0 JWTs](http://gspread.readthedocs.org/en/latest/oauth2.html)
* Save the JWTs file into working directory
* In the working directory, run `pipenv install` to make the virtualenv


## How to deploy?
1. Install [heroku cli](https://devcenter.heroku.com/articles/heroku-cli)
2. Login to heroku by `heroku login`
3. Create new app
4. Go to tab setting, choose `Reveal Config Vars` to set environment variables follow ``.env`` file
5. Use command: `heroku container:push --app <PROJECT_NAME> web` to build and push docker file
6. Use command: `heroku container:release --app <PROJECT_NAME> web` to release this app
7. Done! Go to telegram bot to check the result.
