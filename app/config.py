from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env",
                                      env_file_encoding="utf-8")

    database_hostname: str = "postgres"
    database_port: str = "postgres"
    database_password: str = "localhost"
    database_name: str = "postgres"
    database_username: str = "postgres"
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int


settings = Settings()
