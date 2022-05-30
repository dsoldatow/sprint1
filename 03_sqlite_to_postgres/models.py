import datetime

import uuid

from dataclasses import dataclass
import inspect


# Чтоб пропускать поля, которых нет в моделе
class DataClassFromDict:
    @classmethod
    def from_dict(cls, env):
        return cls(**{
            k: v for k, v in env.items()
            if k in inspect.signature(cls).parameters
        })


@dataclass
class CreatedMixIn:
    created: datetime.datetime = datetime.datetime.now()


@dataclass
class ModifiedMixIn:
    modified: datetime.datetime = datetime.datetime.now()


@dataclass
class IdMixIn:
    id: uuid.UUID


@dataclass
class Filmwork(DataClassFromDict):
    id: uuid.UUID
    title: str
    description: str
    creation_date: datetime.date
    # Ещё один бонус: в dataclass вы можете определить значение по умолчанию
    rating: float
    created: datetime.datetime = datetime.datetime.now()
    modified: datetime.datetime = datetime.datetime.now()

    @classmethod
    @property
    def table(cls):
        return 'film_work'


@dataclass
class Genre(DataClassFromDict):
    id: uuid.UUID
    name: str
    description: str
    created: datetime.datetime = datetime.datetime.now()
    modified: datetime.datetime = datetime.datetime.now()

    @classmethod
    @property
    def table(cls):
        return 'genre'


@dataclass
class Person(IdMixIn, DataClassFromDict):
    full_name: str
    created: datetime.datetime = datetime.datetime.now()
    modified: datetime.datetime = datetime.datetime.now()

    @classmethod
    @property
    def table(cls):
        return 'person'


@dataclass
class GenreFilmWork(IdMixIn, DataClassFromDict):
    genre_id: uuid.UUID
    film_work_id: uuid.UUID
    created: datetime.datetime = datetime.datetime.now()

    @classmethod
    @property
    def table(cls):
        return 'genre_film_work'


@dataclass
class PersonFilmWork(IdMixIn, DataClassFromDict):
    person_id: uuid.UUID
    film_work_id: uuid.UUID
    role: str
    created: datetime.datetime = datetime.datetime.now()

    @classmethod
    @property
    def table(cls):
        return 'person_film_work'


@dataclass
class Data:
    table: str
    data: list


table_to_columns = {
    'film_work': ['id', 'title', 'description', 'rating', 'created', 'modified'],
    'genre': ['id', 'name', 'description', 'created', 'modified'],
    'person': ['id', 'full_name', 'created', 'modified'],
    'genre_film_work': ['id', 'genre_id', 'film_work_id', 'created'],
    'person_film_work': ['id', 'film_work_id', 'person_id', 'role', 'created'],
}

table_to_models = {
    Filmwork.table: Filmwork,
    Genre.table: Genre,
    Person.table: Person,
    GenreFilmWork.table: GenreFilmWork,
    PersonFilmWork.table: PersonFilmWork,
}
