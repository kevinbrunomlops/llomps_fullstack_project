from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    openrouter_api_key: str = Field(default="", alias="OPENROUTER_API_KEY")
    openrouter_base_url: str = Field(default="https://openrouter.ai/api/v1", alias="OPENROUTER_BASE_URL")
    google_maps_api_key: str = Field(default="", alias="GOOGLE_MAPS_API_KEY")
    mlflow_experiment_name: str = Field(default="travel_chatbot_scandinavia", alias="MLFLOW_EXPERIMENT_NAME")
    mlflow_tracking_db_filename: str = Field(default="mlflow.db", alias="MLFLOW_TRACKING_DB_FILENAME")
    prompt_name_system: str = Field(default="travel_chatbot_system_prompt", alias="PROMPT_NAME_SYSTEM")
    prompt_name_tool_dataset: str = Field(default="travel_dataset_lookup_description", alias="PROMPT_NAME_TOOL_DATASET")
    prompt_name_tool_google_maps: str = Field(default="travel_google_maps_lookup_description", alias="PROMPT_NAME_TOOL_GOOGLE_MAPS")
    app_env: str = Field(default="dev", alias="APP_ENV")
    app_name: str = Field(default="travel-chatbot-scandinavia", alias="APP_NAME")
    request_timeout_seconds: int = Field(default=20, alias="REQUEST_TIMEOUT_SECONDS")
    google_maps_max_results: int = Field(default=5, alias="GOOGLE_MAPS_MAX_RESULTS")
    use_google_maps: bool = Field(default=True, alias="USE_GOOGLE_MAPS")
    use_seed_data_fallback: bool = Field(default=True, alias="USE_SEED_DATA_FALLBACK")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @property
    def project_root(self) -> Path:
        return Path(__file__).resolve.parents[2]
    
    @property
    def monitoring_path(self) -> Path:
        return self.project_root / "monitoring"
    
    @property
    def data_path(self) -> Path:
        return self.project_root / "data"
    
    @property
    def tracking_uri(self) -> str:
        return f"sqlite:///{self.monitoring_path / self.mlflow_tracking_db_filename}"
    
@lru_cache
def get_settings() -> Settings:
    return Settings()