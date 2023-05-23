class Config:
    DEBUG = False
    TESTING = False
    # SQLALCHEMY_DATABASE_URI = "sqlite:///myapp.db"
    SECRET_KEY = "604712a91c3108162b651fc80d8b3093"
    LOG_FILE = "logs.log"


# class ProductionConfig(Config):
#     SQLALCHEMY_DATABASE_URI = "postgresql://user:password@localhost/myapp"


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
