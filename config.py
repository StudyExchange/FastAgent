from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "FastAgent"
    version: str = "0.1"
    max_retry: int = 3
    timeout: int = 60
    llm_temperature: float = 0.7
    llm_top_p: float = 0.9
    llm_max_tokens4output: int = 1500
    openai_api_key: str = ""
    openai_base_url: str = ""
    openai_model_name: str = "gpt-4o-mini"
    base_url: str = "127.0.0.1:8000"
    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
