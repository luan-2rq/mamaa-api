import psycopg2
import os

class PostgresRepository:
    def get_connection():
        try:
            connection = psycopg2.connect(user=os.getenv('POSTGRES_USER'),
                                          password=os.getenv('POSTGRES_PASSWORD'),
                                          host=os.getenv('POSTGRES_HOST'),
                                          database=os.getenv('POSTGRES_DB'))

            return connection, connection.cursor()
        except:
            return None, None

    def save_stock(stock):
        connection, cursor = PostgresRepository.get_connection()
        if connection is None:
            return False
        try:
            cursor.execute("INSERT INTO stock (name, price, timestamp) VALUES (%s, %s, %s)", (stock['name'], stock['price'], stock['timestamp']))
            cursor.commit()
            cursor.close()
            connection.close()
            return True
        except:
            return False

        