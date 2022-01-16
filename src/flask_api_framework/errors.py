import http

import flask
import marshmallow


class ApiError(Exception):
    def __init__(self, status_code, **kwargs):
        self.status_code = status_code
        self.kwargs = kwargs

    def get_error_name(self):
        try:
            return http.HTTPStatus(self.status_code).name
        except ValueError:
            return "UNKNOWN"

    def to_dict(self):
        data = dict(
            status=self.status_code,
            name=self.get_error_name(),
            **self.kwargs,
        )
        if isinstance(self.__cause__, marshmallow.ValidationError):
            data["messages"] = self.__cause__.messages
        return data


def api_error_handler(_, e):
    return flask.jsonify(e.to_dict()), e.status_code
