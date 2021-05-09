import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY")

    @staticmethod
    def init_app(app):
        pass


class DockerConfig(Config):
    mysql_pass = os.environ.get("MYSQL_PASSWORD") or ""
    mysql_user = os.environ.get("MYSQL_USER") or ""
    mysql_db = os.environ.get("MYSQL_DATABASE") or ""
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{mysql_user}:{mysql_pass}@db/{mysql_db}"
    )

    @classmethod
    def init_app(cls, app):
        # log to stderr
        import logging
        from logging import StreamHandler

        file_handler = StreamHandler()
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)


config = {"docker": DockerConfig}
