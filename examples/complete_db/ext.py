import flask_marshmallow
import flask_sqlalchemy

import flask_api_framework


db = flask_sqlalchemy.SQLAlchemy()
ma = flask_marshmallow.Marshmallow()
af = flask_api_framework.ApiFramework()
