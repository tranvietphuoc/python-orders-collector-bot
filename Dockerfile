FROM python:3.8.2

RUN pip install flask pyTelegramBotAPI python-dotenv oauth2client gspread gunicorn
RUN mkdir /app
ADD . /app
WORKDIR /app

CMD gunicorn run:app --preload -w 1