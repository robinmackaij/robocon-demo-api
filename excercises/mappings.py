from typing import Type

from OpenApiLibCore import (
    IGNORE,
    Dto,
    IdDependency,
    IdReference,
    PathPropertiesConstraint,
    PropertyValueConstraint,
    Relation,
    UniquePropertyValueConstraint,
)


ID_MAPPING = {}


class AuthorDto(Dto):
    @staticmethod
    def get_relations() -> list[Relation]:
        relations: list[Relation] = [
            IdReference(
                property_name="author_id",
                post_path="/poems",
                error_code=403,
            ),
        ]
        return relations


class PoemDto(Dto):
    @staticmethod
    def get_relations() -> list[Relation]:
        relations: list[Relation] = [
            IdDependency(
                property_name="author_id",
                get_path="/authors",
            ),
        ]
        return relations


DTO_MAPPING: dict[tuple[str, str], Type[Dto]] = {
    ("/authors/{author_id}", "delete"): AuthorDto,
    ("/poems", "post"): PoemDto,
}
