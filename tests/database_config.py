from masonite.environment import LoadEnvironment, env
from masoniteorm.connections import ConnectionResolver

#  Loads in the environment variables when this page is imported.
LoadEnvironment()

"""
The connections here don't determine the database but determine the "connection".
They can be named whatever you want.
"""
DATABASES = {
    "default": env("DB_CONNECTION_TEST", "postgres_test"),
     "postgres_test": {
        "driver": "postgres",
        "host": env("DB_HOST_TEST"),
        "user": env("DB_USERNAME_TEST"),
        "password": env("DB_PASSWORD_TEST"),
        "database": env("DB_DATABASE_TEST"),
        "port": env("DB_PORT_TEST"),
        "prefix": "",
        "grammar": "postgres",
        "log_queries": env("DB_LOG"),
    },
}

DB = ConnectionResolver().set_connection_details(DATABASES)
