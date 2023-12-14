import sqlite3


def connect_to_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn


def initial_setup():
    conn = connect_to_db()
    conn.execute(
        """
        DROP TABLE IF EXISTS songs;
        """
    )
    conn.execute(
        """
        CREATE TABLE songs (
          id INTEGER PRIMARY KEY NOT NULL,
          title STRING,
          album STRING,
          duration STRING,
          artist_id INTEGER,
          FOREIGN KEY (artist_id) REFERENCES artists(id)
        );
        """
    )
    conn.commit()
    print("Table created successfully")

    songs_seed_data = [
        ("Free Bird", "Pronounced Leh-Nerd Skin-Nerd", "9:11", 3),
        ("American Girl", "Tom Petty and the Hearbreakers", "3:33", 1),
        ("The Unforgiven", "The Black Box", "6:28", 2),
        ("Wildflowers", "Full Moon", "3:21", 1)
    ]
    conn.executemany(
        """
        INSERT INTO songs (title, album, duration, artist_id)
        VALUES (?,?,?,?)
        """,
        songs_seed_data,
    )

    # Artist db
    conn.execute(
        """
        DROP TABLE IF EXISTS artists;
        """
    )
    conn.execute(
        """
        CREATE TABLE artists (
          id INTEGER PRIMARY KEY NOT NULL,
          name STRING,
          bio TEXT
        );
        """
    )
    conn.commit()
    print("Table created successfully")

    artists_seed_data = [
        ("Tom Petty", "From Florida"),
        ("Metallica", "From Oregon"),
        ("Lynyrd Skynyrd", "From Alabama"),
    ]
    conn.executemany(
        """
        INSERT INTO artists (name, bio)
        VALUES (?,?)
        """,
        artists_seed_data,
    )
    
    conn.commit()
    print("Seed data created successfully")

    conn.close()

def songs_all():
    conn = connect_to_db()
    rows = conn.execute(
        """
        SELECT songs.*, artists.name AS artist_name, artists.bio AS artist_bio FROM songs
        JOIN artists ON songs.artist_id = artists.id
        """
    ).fetchall()
    return [dict(row) for row in rows]

def songs_create(title, album, duration, artist_id):
    conn = connect_to_db()
    row = conn.execute(
        """
        INSERT INTO songs (title, album, duration, artist_id)
        VALUES (?, ?, ?, ?)
        RETURNING *
        """,
        (title, album, duration, artist_id),
    ).fetchone()
    conn.commit()
    return dict(row)

def songs_find_by_id(id):
    conn = connect_to_db()
    row = conn.execute(
        """
        SELECT * FROM songs
        WHERE id = ?
        """,
        id,
    ).fetchone()
    return dict(row)

def songs_update_by_id(id, title, album, duration, artist_id):
    conn = connect_to_db()
    row = conn.execute(
        """
        UPDATE songs SET title = ?, album = ?, duration = ?, artist_id = ?
        WHERE id = ?
        RETURNING *
        """,
        (title, album, duration, artist_id, id),
    ).fetchone()
    conn.commit()
    return dict(row)

def songs_destroy_by_id(id):
    conn = connect_to_db()
    row = conn.execute(
        """
        DELETE from songs
        WHERE id = ?
        """,
        id,
    )
    conn.commit()
    return {"message": "Song destroyed successfully"}


# Artist methods
def artists_all():
    conn = connect_to_db()
    rows = conn.execute(
        """
        SELECT artists.*, GROUP_CONCAT(songs.title, ", ") AS songslist
        FROM artists
        JOIN songs ON artists.id = songs.artist_id
        GROUP BY artists.id
        """
    ).fetchall()
    return [dict(row) for row in rows]

def artists_create(name, bio):
    conn = connect_to_db()
    row = conn.execute(
        """
        INSERT INTO artists (name, bio)
        VALUES (?, ?)
        RETURNING *
        """,
        (name, bio),
    ).fetchone()
    conn.commit()
    return dict(row)

def artists_find_by_id(id):
    conn = connect_to_db()
    row = conn.execute(
        """
        SELECT artists.*, GROUP_CONCAT(songs.title, ", ") AS songslist
        FROM artists
        JOIN songs ON artists.id = songs.artist_id
        WHERE artists.id = ?
        GROUP BY artists.id
        """,
        id,
    ).fetchone()
    return dict(row)

def artists_update_by_id(id, name, bio):
    conn = connect_to_db()
    row = conn.execute(
        """
        UPDATE artists SET name = ?, bio = ?
        WHERE id = ?
        RETURNING *
        """,
        (name, bio, id),
    ).fetchone()
    conn.commit()
    return dict(row)

def artists_destroy_by_id(id):
    conn = connect_to_db()
    row = conn.execute(
        """
        DELETE from artists
        WHERE id = ?
        """,
        id,
    )
    conn.commit()
    return {"message": "Artist destroyed successfully"}

if __name__ == "__main__":
    initial_setup()