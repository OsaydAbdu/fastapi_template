import re
from typing import Any

from sqlalchemy.ext.declarative import as_declarative, declared_attr


def camel_case_to_snake_case(s):
    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", s)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()


@as_declarative()
class Base:
    id: Any
    __name__: str
    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return camel_case_to_snake_case(cls.__name__)

    def to_dict(self):
        """
        Convert the DB Model to a dictionary that includes non-relationship columns only
        """
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __str__(self):
        return str(self.to_dict())

    def __repr__(self):
        return str(self)
