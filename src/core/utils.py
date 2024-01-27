from datetime import datetime

from sqlalchemy import inspect

from core.db import Base


def model_to_dict(model: Base) -> dict:
    model_dict = {c.key: getattr(model, c.key) for c in inspect(model).mapper.column_attrs}
    for key, value in model_dict.items():
        if isinstance(value, datetime):
            model_dict[key] = value.isoformat()
    return model_dict
