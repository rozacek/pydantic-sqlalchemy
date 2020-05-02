from typing import Type

from pydantic import BaseConfig, BaseModel, create_model
from sqlalchemy.inspection import inspect
from sqlalchemy.orm.properties import ColumnProperty


class OrmConfig(BaseConfig):
    orm_mode = True


def sqlalchemy_to_pydantic(db_model: Type) -> Type[BaseModel]:
    mapper = inspect(db_model)
    fields = {}
    for attr in mapper.attrs:
        if isinstance(attr, ColumnProperty):
            if attr.columns:
                column = attr.columns[0]
                python_type = column.type.python_type
                name = attr.key
                default = column.default
                if default is None and not column.nullable:
                    default = ...
                fields[name] = (python_type, default)
    pydantic_model = create_model(
        db_model.__name__, __config__=OrmConfig, **fields  # type: ignore
    )
    return pydantic_model
