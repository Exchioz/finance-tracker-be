from pydantic_settings import BaseSettings

class Settings(BaseSettings):

    environment: str = "development"
    app_port: int

    postgres_user: str
    postgres_password: str
    postgres_host: str
    postgres_port: int
    postgres_db: str

    secret_key: str
    algorithm: str
    access_token_expire: int

    @property
    def database_url(self) -> str:
        return f"postgresql://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        from_attributes = True
        
settings = Settings()