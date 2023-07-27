"""
Archivo para la conexión FTP
"""
from ftplib import FTP
import psycopg2
def create_ftp_connection() -> FTP:
    host = "192.168.56.101"
    user = "juankar"
    passwd = "123456"
    
    ftp = FTP(host)
    ftp.login(user=user, passwd=passwd)

    return ftp

def create_postgres_connection() -> psycopg2.extensions.connection:
    host="localhost"
    database="bandam"
    user="postgres"
    password="123456"
    conn = psycopg2.connect(
        host=host,
        database=database,
        user=user,
        password=password
    )

    return conn