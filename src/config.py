from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_HOST: str
    DB_NAME: str
    DB_PORT: int
    DB_USER: str
    DB_PWD: str
    SECRET_TOKEN: str
    PUBLIC_TOKEN: str
    DOMAIN: str

    class Config:
        env_file = ".env"

    @property
    def db_url(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PWD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


settings = Settings()
