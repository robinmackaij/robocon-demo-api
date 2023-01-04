import sqlite3
from uuid import UUID, uuid4

from robocon_demo_api.models.author import Author
from robocon_demo_api.models.poem import Poem


CONNECTION = sqlite3.connect("workshop.db")
CURSOR = CONNECTION.cursor()


CURSOR.execute("CREATE TABLE IF NOT EXISTS authors(id PRIMARY KEY, name, bio, species)")
CURSOR.execute("CREATE TABLE IF NOT EXISTS poems(id PRIMARY KEY, title, content, author_id, FOREIGN KEY(author_id) REFERENCES authors(id))")

default = CURSOR.execute(
    "SELECT * FROM authors WHERE name='unknown author' AND species='unknown'"
)
if default.fetchone() is None:
    CURSOR.execute(f"""
        INSERT INTO authors VALUES
            ('{uuid4()}', 'unknown author', ?, 'unknown')
    """, (None,))
    CONNECTION.commit()


def store_poem(poem: Poem) -> None:
    connection = sqlite3.connect("workshop.db")
    cursor = connection.cursor()
    result = cursor.execute(
        f"SELECT * FROM authors WHERE id='{poem.author_id}'"
    )
    if result.fetchone() is None:
        raise ValueError("AuthorNotFound", f"Author with author_id {poem.author_id} does not exist.")

    cursor.execute(f"""
        INSERT INTO poems VALUES
            ('{poem.id}', '{poem.title}', '{poem.content}', '{poem.author_id}')
    """)
    connection.commit()


def get_poems() -> list[Poem]:
    connection = sqlite3.connect("workshop.db")
    cursor = connection.cursor()
    result = cursor.execute("SELECT * FROM poems")
    result_list = result.fetchall()
    return [get_poem_from_tuple(poem_data) for poem_data in result_list]


def get_poem(poem_id: UUID) -> Poem | None:
    connection = sqlite3.connect("workshop.db")
    cursor = connection.cursor()
    result = cursor.execute(f"SELECT * FROM poems WHERE id = '{poem_id}'")
    result_list = result.fetchall()
    if not result_list:
        return None
    return get_poem_from_tuple(result_list[0])


def get_poem_from_tuple(poem_tuple: tuple[str, str, str, str]) -> Poem:
    return Poem(
        id=poem_tuple[0],
        title=poem_tuple[1],
        content=poem_tuple[2],
        author_id=poem_tuple[3],
    )


def store_author(author: Author) -> None:
    connection = sqlite3.connect("workshop.db")
    cursor = connection.cursor()
    cursor.execute(f"""
        INSERT INTO authors VALUES
            ('{author.id}', '{author.name}', '{author.bio}', '{author.species.value}')
    """)
    connection.commit()


def get_authors() -> list[Author]:
    connection = sqlite3.connect("workshop.db")
    cursor = connection.cursor()
    result = cursor.execute("SELECT * FROM authors")
    result_list = result.fetchall()
    return [get_author_from_tuple(author_data) for author_data in result_list]


def get_author(author_id: UUID) -> Author | None:
    connection = sqlite3.connect("workshop.db")
    cursor = connection.cursor()
    result = cursor.execute(f"SELECT * FROM authors WHERE id = '{author_id}'")
    result_list = result.fetchall()
    if not result_list:
        return None
    return get_author_from_tuple(result_list[0])


def get_author_from_tuple(author_tuple: tuple[str, str, str, str]) -> Author:
    return Author(
        id=author_tuple[0],
        name=author_tuple[1],
        bio=author_tuple[2],
        species=author_tuple[3],
    )
