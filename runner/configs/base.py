import pydantic

from runner.configs.environment_avaliable import EnvironmentAvaliable


class ConfigApp(pydantic.BaseSettings):
    db_name: str
    db_user: str
    db_host: str
    db_port: int
    db_password: str
    environment: EnvironmentAvaliable
    is_docker: bool = False

    class Config:
        extra = "ignore"
