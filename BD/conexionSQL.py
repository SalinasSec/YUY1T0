from mysql.connector import connect, Error

# ------------------ MYSQL ------------------


class DAO:
    @staticmethod
    def yconectar():
        try:
            return connect(
                host="localhost",
                user="root",
                password="abcd1234",
                database="clinica",
            )
        except Error as ex:
            print("Error conectar base de datos", ex)
