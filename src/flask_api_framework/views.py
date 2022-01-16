import flask
import flask.views
import marshmallow
import sqlalchemy

from .errors import ApiError
from .helpers import getattr_fallback, is_sa_mapped


class BaseViewType(type):
    def __init__(cls, name, bases, d):
        super().__init__(name, bases, d)

        if "methods" not in d:
            methods = set()

            for base in bases:
                if getattr(base, "methods", None):
                    methods.update(base.methods)

            for key in flask.views.http_method_funcs:
                if hasattr(cls, f"handle_{key}"):
                    methods.add(key.upper())

            cls.methods = methods

        actions = ["list", "read", "create", "update", "delete"]
        schema_names = {
            "{action}_kwargs": ["kwargs"],
            "{action}_args": ["args"],
            "{action}_request_body": ["request_body", "{action}_body", "body"],
            "{action}_response_body": ["response_body", "{action}_body", "body"],
        }
        for _ in bases:
            for action in actions:
                for name, fallbacks in schema_names.items():
                    name = f"{name}_schema".format(action=action)
                    fallbacks = [
                        f"{fallback}_schema".format(action=action)
                        for fallback in fallbacks
                    ]
                    attr = getattr_fallback(cls, name, *fallbacks)
                    if attr is not None:
                        setattr(cls, name, attr)


class BaseView(flask.views.View, metaclass=BaseViewType):
    kwargs_schema = None
    args_schema = None
    body_schema = None

    loaded_kwargs = None
    loaded_args = None

    @property
    def db(self):
        return flask.current_app.extensions["api-framework"].db

    def dispatch_request(self, *args, **kwargs):
        try:
            method = flask.request.method.lower()
            handler = getattr(self, f"handle_{method}", None)
            return flask.current_app.ensure_sync(handler)(*args, **kwargs)
        except marshmallow.exceptions.ValidationError as e:
            raise ApiError(status_code=400, source="body") from e

    def load_kwargs_schema(self):
        self.loaded_kwargs = self.kwargs_schema.load(data=flask.request.view_args)

    def load_args_schema(self):
        self.loaded_args = self.args_schema.load(data=flask.request.args)

    def handle_kwargs(self, schema):
        try:
            if schema is not None:
                self.kwargs_schema = schema
                self.load_kwargs_schema()
        except marshmallow.exceptions.ValidationError as e:
            raise ApiError(status_code=400, source="kwargs") from e
        if (
            is_sa_mapped(self.loaded_kwargs)
            and sqlalchemy.inspect(self.loaded_kwargs).transient
        ):
            raise ApiError(status_code=404)

    def handle_args(self, schema):
        try:
            if schema is not None:
                self.args_schema = schema
                self.load_args_schema()
        except marshmallow.exceptions.ValidationError as e:
            raise ApiError(status_code=400, source="args") from e
        if (
            is_sa_mapped(self.loaded_args)
            and sqlalchemy.inspect(self.loaded_args).transient
        ):
            raise ApiError(status_code=404)

    def get_schema_success_data(
        self,
        schema,
        data,
        status_code=200,
        data_wrapper=None,
        many=False,
    ):
        def noop_data_wrapper(x):
            return x

        if data_wrapper is None:
            data_wrapper = noop_data_wrapper
        if schema is not None:
            return (
                flask.jsonify(data_wrapper(schema.dump(data, many=many))),
                status_code,
            )
        elif schema is None and data is not None:
            return flask.jsonify(data_wrapper(data)), status_code
        else:
            return "", 204


class List(BaseView):
    list_kwargs_schema = None
    list_args_schema = None
    list_body_schema = None
    list_response_body_schema = None
    response_body_schema = None

    instances = None

    def handle_get(self, *args, **kwargs):
        self.handle_kwargs(self.list_kwargs_schema)
        self.handle_args(self.list_args_schema)
        self.instances = self.get_instances()
        return self.get_list_response()

    def get_instances(self):
        return []

    def get_list_response(self):
        return self.get_schema_success_data(
            schema=self.list_response_body_schema,
            data=self.instances,
            data_wrapper=lambda data: dict(items=data),
            many=True,
        )


class Read(BaseView):
    read_kwargs_schema = None
    read_args_schema = None
    read_body_schema = None
    read_response_body_schema = None
    response_body_schema = None

    instance = None

    def handle_get(self, *args, **kwargs):
        self.handle_kwargs(self.read_kwargs_schema)
        self.handle_args(self.read_args_schema)
        self.instance = self.get_instance()
        return self.get_read_response()

    def get_instance(self):
        return self.loaded_kwargs

    def get_read_response(self):
        return self.get_schema_success_data(
            schema=self.read_response_body_schema,
            data=self.instance,
        )


class Create(BaseView):
    create_kwargs_schema = None
    create_args_schema = None
    create_body_schema = None
    create_request_body_schema = None
    create_response_body_schema = None
    request_body_schema = None
    response_body_schema = None

    loaded_body = None
    instance = None

    def handle_post(self, *args, **kwargs):
        self.handle_kwargs(self.create_kwargs_schema)
        self.handle_args(self.create_args_schema)
        if self.create_request_body_schema is not None:
            self.body_schema = self.create_request_body_schema
            self.load_create_request_body_schema()
        self.instance = self.create()
        self.db.session.commit()
        return self.get_create_response()

    def load_create_request_body_schema(self):
        self.loaded_body = self.create_request_body_schema.load(data=flask.request.json)

    def create(self):
        if is_sa_mapped(self.loaded_body):
            self.db.session.add(self.loaded_body)
        return self.loaded_body

    def get_create_response(self):
        return self.get_schema_success_data(
            schema=self.create_response_body_schema,
            data=self.instance,
            status_code=201,
        )


class Update(BaseView):
    update_kwargs_schema = None
    update_args_schema = None
    update_body_schema = None
    update_request_body_schema = None
    update_response_body_schema = None
    request_body_schema = None
    response_body_schema = None

    loaded_body = None
    instance = None

    def handle_patch(self, *args, **kwargs):
        return self.handle_update(*args, partial=True, **kwargs)

    def handle_put(self, *args, **kwargs):
        return self.handle_update(*args, partial=False, **kwargs)

    def handle_update(self, *args, partial, **kwargs):
        self.handle_kwargs(self.update_kwargs_schema)
        self.handle_args(self.update_args_schema)
        self.instance = self.get_instance()
        if self.update_request_body_schema is not None:
            self.body_schema = self.load_update_request_body_schema
            self.load_update_request_body_schema(partial=partial)
        self.instance = self.update()
        self.db.session.commit()
        return self.get_update_response()

    def get_instance(self):
        return self.loaded_kwargs

    def load_update_request_body_schema(self, partial):
        kwargs = dict(
            data=flask.request.json,
            partial=partial,
        )
        if self.get_schema_load_instance(self.update_request_body_schema):
            kwargs["instance"] = self.instance
        self.loaded_body = self.update_request_body_schema.load(**kwargs)

    def get_schema_load_instance(self, schema):
        try:
            return schema.Meta.load_instance
        except AttributeError:
            return False

    def update(self):
        return self.instance

    def get_update_response(self):
        return self.get_schema_success_data(
            schema=self.update_response_body_schema,
            data=self.instance,
        )


class Delete(BaseView):
    delete_kwargs_schema = None
    delete_args_schema = None
    delete_body_schema = None
    delete_response_body_schema = None
    response_body_schema = None

    instance = None

    def handle_delete(self, *args, **kwargs):
        self.handle_kwargs(self.delete_kwargs_schema)
        self.handle_args(self.delete_args_schema)
        self.instance = self.get_instance()
        self.instance = self.delete()
        self.db.session.commit()
        return self.get_delete_response()

    def get_instance(self):
        return self.loaded_kwargs

    def delete(self):
        if is_sa_mapped(self.instance):
            self.db.session.delete(self.instance)
        return self.instance

    def get_delete_response(self):
        return self.get_schema_success_data(
            schema=self.delete_response_body_schema,
            data=self.instance,
        )
