class base:
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    JSON_SORT_KEYS = False
    FLASK_ADMIN_FLUID_LAYOUT = True
    FLASK_ADMIN_SWATCH = "yeti"


class test(base):
    TESTING = True
