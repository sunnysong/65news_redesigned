
import os
import psycopg2


# urlparse.uses_netloc.append("postgres")
# url = urlparse.urlparse(os.environ["DATABASE_URL"])

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'findhowtomakeasecretekey'
    POSTS_PER_PAGE = 10
    SQLALCHEMY_DATABASE_URI = "postgres://tgyfurejthgdua:xHsGpxXUfR-mbdd2hGNH78Jn97@ec2-54-83-20-177.compute-1.amazonaws.com:5432/dfi4f30499l1s8" or os.environ.get('SQLALCHEMY_DATABASE_URL') or os.environ["DATABASE_URL"]

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
