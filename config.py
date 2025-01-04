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
    openai_embedding_name: str = "text-embedding-3-small"
    vector_dim: int = 128
    max_distance4rag: float = 0.4
    neo4j_url: str = ""
    lightrag_working_dir: str = "./dickens"
    lightrag_docs_dir: str = "./tests/assets/rag_docs"
    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
