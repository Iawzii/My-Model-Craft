from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


load_dotenv()


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore", case_sensitive=False)

    app_name: str = Field(default="Model Craft API", alias="APP_NAME")
    database_url: str = Field(alias="DATABASE_URL")
    jwt_secret_key: str = Field(alias="JWT_SECRET_KEY")
    jwt_algorithm: str = Field(default="HS256", alias="JWT_ALGORITHM")
    jwt_expires_minutes: int = Field(default=60 * 24, alias="JWT_EXPIRES_MINUTES")
    verification_code_length: int = Field(default=6, alias="VERIFICATION_CODE_LENGTH")
    verification_code_exp_minutes: int = Field(default=10, alias="VERIFICATION_CODE_EXP_MINUTES")
    smtp_host: str = Field(default="smtp.qq.com", alias="SMTP_HOST")
    smtp_port: int = Field(default=465, alias="SMTP_PORT")
    smtp_user: str = Field(alias="SMTP_USER")
    smtp_password: str = Field(alias="SMTP_PASSWORD")


settings = Settings()
