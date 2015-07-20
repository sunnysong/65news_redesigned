import os

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'findhowtomakeasecretekey'
    POSTS_PER_PAGE = 10
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URL') or 'postgres://vhuvzbqunrckxz:GdYjT1oIe3urNuE5Xf7x7LgLc-@ec2-54-83-20-177.compute-1.amazonaws.com:5432/d9sj9dn3q67lei' 

    @staticmethod
    def init_app(app):
        pass


class ProductionConfig(Config):
    DEBUG = False



class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'staging': StagingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
