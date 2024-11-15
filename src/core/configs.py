from pydantic_settings import BaseSettings, SettingsConfigDict


class Configs(BaseSettings):
    VERSION: str = "v1"
    CHROMA_PATH: str
    DATA_PATH: str

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )
