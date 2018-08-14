import os


class Config:
    """
    Common configurations
    Put any configurations here that are common across all environments
    """
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_AUTH_URL_RULE = "/api/v1/login"


class DevelopmentConfig(Config):
    """
    Development configurations
    """
    DB_PATH = os.path.join(os.path.dirname(__file__), 'database.db')
    DEBUG = True
#    SQLALCHEMY_ECHO = True
    SECRET_KEY = "FakeK3y"
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{DB_PATH}"


class TestingConfig(Config):
    """
    Testing configurations
    """
    TESTING = True


class ProductionConfig(Config):
    """
    Production configurations
    """

app_config = {
        'development': DevelopmentConfig,
        'production': ProductionConfig,
        'testing': TestingConfig,
        }
