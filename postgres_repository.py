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
        print('salvando stock no banco de dados')
        connection, cursor = PostgresRepository.get_connection()
        if connection is None:
            print('não foi possivel conectar ao banco de dados')
            return False
        try:
            cursor.execute("INSERT INTO stock (name, price, timestamp) VALUES (%s, %s, %s)", (stock['name'], stock['price'], stock['timestamp']))
            cursor.commit()
            cursor.close()
            connection.close()
            return True
        except Exception as e:
            print(e)
            return False
        
    def get_stock_history():
        connection, cursor = PostgresRepository.get_connection()
        if connection is None:
            return None
        try:
            cursor.execute("SELECT * FROM stock")
            stock_history = cursor.fetchall()
            cursor.close()
            connection.close()
            return stock_history
        except:
            return None
        
    def get_stock_history_by_name(name):
        connection, cursor = PostgresRepository.get_connection()
        if connection is None:
            return None
        try:
            cursor.execute("SELECT * FROM stock WHERE name = %s", (name,))
            stock_history = cursor.fetchall()
            cursor.close()
            connection.close()
            return stock_history
        except:
            return None

        