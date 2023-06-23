"""
Archivo para la conexión FTP
"""
from ftplib import FTP

def create_ftp_connection() -> FTP:
    host = "192.168.56.101"
    user = "juankar"
    passwd = "123456"
    
    ftp = FTP(host)
    ftp.login(user=user, passwd=passwd)

    return ftp
