import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    DEBUG = True
    # Création du fichier SQLite à la racine du projet
    SQLALCHEMY_DATABASE_URI = 'sqlite:///hbnb.dev.db'

class ProductionConfig(Config):
    DEBUG = False
    SECRET_KEY = "prod_secret_key"
    SQLALCHEMY_DATABASE_URI = 'sqlite:///hbnb.db'

config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig,
    'production': ProductionConfig,
}


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"  
    SQLALCHEMY_TRACK_MODIFICATIONS = False

config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig  
}
