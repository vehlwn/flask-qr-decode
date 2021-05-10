import os



class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

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
        pass


config = {"docker": DockerConfig}
