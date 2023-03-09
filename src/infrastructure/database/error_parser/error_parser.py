from sqlalchemy.exc import IntegrityError

from typing import Type, List, Dict

from src.domain.common.entities.entity import Entity

from src.infrastructure.database.error_parser.exception_returner import ExceptionReturner


class ErrorParser:

    def __init__(self):
        self._exception_returners: List[ExceptionReturner] = []

    def _get_returner(self, entity: Type[Entity], database_column: str):
        for returner in self._exception_returners:
            if returner.check(database_column, entity):
                return returner

    def add_exception_returner(self, entity: Type[Entity], func, database_column):
        self._exception_returners.append(ExceptionReturner(func=func, database_column=database_column, entity=entity))

    def parse_error(self, entity: Entity, exception: IntegrityError):
        database_column = exception.__cause__.__cause__.constraint_name
        returner = self._get_returner(type(entity), database_column)
        return returner.return_exception(entity)
