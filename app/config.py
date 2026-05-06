from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    hostname : str
    username : str
    name : str
    port: str
    password : str
    algorithm : str
    secret_key : str
    access_token_expire_minutes: int
    model_config = {'env_file': '.env'}


settings = Settings()  