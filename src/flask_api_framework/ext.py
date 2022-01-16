from . import errors, views


class ApiFramework:
    List = views.List
    Read = views.Read
    Create = views.Create
    Update = views.Update
    Delete = views.Delete
    ApiError = errors.ApiError
    api_error_handler = errors.api_error_handler

    def __init__(self, app=None, *args, **kwargs):
        if app is not None:
            self.init_app(app, *args, **kwargs)

    def init_app(self, app, db=None):
        self.db = db
        app.extensions["api-framework"] = self
