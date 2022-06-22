import os


class Config:
    SECRET_KEY = os.environ["SECRET_KEY"]

    @staticmethod
    def init_app(app):
        pass


class DockerConfig(Config):
    mongo_user = os.environ["MONGO_USER"]
    mongo_password = os.environ["MONGO_PASSWORD"]
    mongo_db = os.environ["MONGO_DATABASE"]
    MONGO_URI = f"mongodb://{mongo_user}:{mongo_password}@db:27017/{mongo_db}"

    @classmethod
    def init_app(cls, app):
        pass


config = {"docker": DockerConfig}
