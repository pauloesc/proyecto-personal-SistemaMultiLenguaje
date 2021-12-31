class Config(object):
    SECRET_KEY = 'LosMalosNoDuermen'

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:@localhost/flask'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
