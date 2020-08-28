from dotenv import load_dotenv
import os


APP_PATH = os.path.join(os.path.dirname(__file__), ".")
ENV_PATH = os.path.join(APP_PATH, ".env")
# load_dotenv(ENV_PATH, verbose=True, override=True)

# TOKEN = os.environ.get("TOKEN")
# SECRET_KEY = os.environ.get("SECRET_KEY")
# PROJECT = os.environ.get("PROJECT")

TOKEN = os.getenv("TOKEN")
SECRET_KEY = os.getenv("SECRET_KEY")
PROJECT = os.getenv("PROJECT")
SPREADSHEETS_ID = os.getenv('SPREADSHEETS_ID')
