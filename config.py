from dotenv import load_dotenv
import os


APP_PATH = os.path.join(os.path.dirname(__file__), ".")
ENV_PATH = os.path.join(APP_PATH, ".env")
load_dotenv(ENV_PATH, verbose=True, override=True)

TOKEN = os.getenv("TOKEN")
SECRET_KEY = os.getenv("SECRET_KEY")
PROJECT = os.getenv("PROJECT")
