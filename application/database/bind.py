from peewee_async import Manager, PooledPostgresqlDatabase

from runner.configs import config

database = PooledPostgresqlDatabase(
    database=config.db_name,
    user=config.db_user,
    host=config.db_host,
    port=int(config.db_port),
    password=config.db_password,
    autoconnect=True,
    connection_timeout=30,
)

db_manager = Manager(database)
