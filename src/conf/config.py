import configparser
import os



class Config():
    '''
    Classe di utils per il file config
    '''
    def __init__(self):
        name = os.path.abspath( os.path.join( __file__ , r"../../conf/properties_prod.ini"))
        #name = os.path.abspath( os.path.join( __file__ , r"../../conf/properties_test.ini"))
        self.config = configparser.ConfigParser()
        self.config._interpolation = configparser.ExtendedInterpolation()
        self.config.read(name)

    def get_db_dbname(self):
        return self.config.get("postgres", "dbname")

    def get_db_username(self):
        return self.config.get("postgres", "username")

    def get_db_password(self):
        return self.config.get("postgres", "password")

    def get_db_host(self):
        return self.config.get("postgres", "host")

    def get_db_port(self):
        return self.config.get("postgres", "port")

    def get_db_url(self):
        return f'postgresql://{self.get_db_username()}:{self.get_db_password()}@{self.get_db_host()}/{self.get_db_dbname()}'

    def get_db_test_url(self):
        return f'postgresql://{self.get_db_username()}:{self.get_db_password()}@localhost:5432/test'

    def get_jwt_secret_key(self):
        return self.config.get("json_web_token", "secret_key")

    def get_jwt_algorithm(self):
        return self.config.get("json_web_token", "algorithm")

    def get_jwt_access_token_expires_minutes(self):
        return self.config.get("json_web_token", "access_token_expires_minutes")

    def get_otp_length(self):
        return self.config.get("otp", "length")

    def get_table_user_declaration(self):
        return os.path.abspath( os.path.join( __file__ , r"../../resources/create_table_user.sql"))

    def get_table_otp_declaration(self):
        return os.path.abspath( os.path.join( __file__ , r"../../resources/create_table_otp.sql"))
