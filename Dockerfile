FROM python:3.8.2

RUN pip install flask pyTelegramBotAPI python-dotenv oauth2client gspread gunicorn pandas df2gspread
RUN mkdir /app
ADD . /app
WORKDIR /app
RUN ls -la

CMD sh start.sh
