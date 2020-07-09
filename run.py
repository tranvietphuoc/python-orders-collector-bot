from app import app
import logging
from logging import Formatter, FileHandler


if __name__ == "__main__":
    file_handler = FileHandler("app.log")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(
        Formatter("%(asctime)s %(levelname)s %(username)s: %(message)s")
    )
    app.logger.addHandler(file_handler)
    app.run(debug=True)
