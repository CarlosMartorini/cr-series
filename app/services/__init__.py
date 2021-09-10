import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

configs = {
    "host": os.environ.get("DB_HOST"),
    "database": os.environ.get("DB_DATABASE"),
    "user": os.environ.get("DB_USER"),
    "password": os.environ.get("DB_PASSWORD")
}


def open_connection():
    return psycopg2.connect(**configs)


def create_table():
    conn = open_connection()

    cur = conn.cursor()

    cur.execute(
        """
            CREATE TABLE IF NOT EXISTS ka_series (
                id BIGSERIAL PRIMARY KEY,
                serie VARCHAR(100) NOT NULL UNIQUE,
                seasons INTEGER NOT NULL,
                released_date DATE NOT NULL,
                genre VARCHAR(50) NOT NULL,
                imdb_rating FLOAT NOT NULL
            );
        """
    )

    conn.commit()
    
    cur.close()
    conn.close()


class Serie:

    
    def __init__(self, data: tuple):
        self.id, serie, self.seasons, released_date, genre, self.imdb_rating = data
        self.serie = serie.title()
        self.released_date = released_date
        self.genre = genre.title()

    
    def create_serie(data):

        conn = open_connection()

        cur = conn.cursor()

        cur.execute(
            """
                INSERT INTO ka_series 
                    (serie, seasons, released_date, genre, imdb_rating)
                VALUES
                    (%s, %s, %s, %s, %s);
            """,
            (data['serie'].title(), data['seasons'], data['released_date'], data['genre'].title(), data['imdb_rating'])
        )

        conn.commit()

        cur.close()
        conn.close()

    
    def return_serie_created(data):
        
        conn = open_connection()
        
        cur = conn.cursor()
        
        cur.execute(
            """
                SELECT * FROM ka_series WHERE serie=(%s)
            """,
            (data['serie'].title(), )
        )
        
        result = cur.fetchone()
        
        conn.commit()
        
        cur.close()
        conn.close()
        
        add_serie = Serie(result).__dict__
        
        return add_serie


    @staticmethod
    def show_all_series():
        conn = open_connection()

        cur = conn.cursor()

        create_table()

        cur.execute(
            """
                SELECT * FROM ka_series;
            """
        )

        result = cur.fetchall()

        conn.commit()

        cur.close()
        conn.close()

        list_series = [Serie(data).__dict__ for data in result]

        return {"data": list_series}

    
    @staticmethod
    def show_specific_serie(id):
        conn = open_connection()

        cur = conn.cursor()

        cur.execute(
            """
                SELECT * FROM ka_series WHERE id=(%s);
            """,
            (id, )
        )

        result = cur.fetchone()

        conn.commit()

        cur.close()
        conn.close()

        serie = Serie(result).__dict__

        return {"data": serie}