from typing import Any, Iterable

import sqlalchemy


def getattr_fallback(
    object: Any,
    name: str,
    *fallbacks: Iterable[str],
    default: Any = None,
) -> Any:
    attr = getattr(object, name, None)
    if attr is not None:
        return attr

    for fallback in fallbacks:
        attr = getattr(object, fallback, None)
        if attr is not None:
            return attr

    return default


def is_sa_mapped(obj):
    try:
        sqlalchemy.orm.object_mapper(obj)
    except sqlalchemy.orm.exc.UnmappedInstanceError:
        return False
    return True
