import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "izy3t2e66a4u6u51p1hc"

    @staticmethod
    def init_app(app):
        pass


config = {"default": Config}
