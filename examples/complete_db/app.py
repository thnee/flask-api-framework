from complete_db.ext import af, db, ma
from flask import Flask
from werkzeug.utils import import_string


def create_app(conf=None):
    app = Flask(__name__)

    if not conf:
        conf = "base"

    config = import_string(f"complete_db.conf.{conf.lower()}")()
    app.config.from_object(config)

    db.init_app(app)
    ma.init_app(app)
    af.init_app(app, db)

    app.errorhandler(af.ApiError)(af.api_error_handler)

    with app.app_context():
        from complete_db import blueprints  # noqa
        from complete_db import models  # noqa

        db.create_all()

    app.register_blueprint(blueprints.api_v1.bp, url_prefix="/v1")

    return app
