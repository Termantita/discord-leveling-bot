from pydantic import (
    Field,
)
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


class Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        env_ignore_empty=True,
        env_parse_none_str="null",
    )

    DISCORD_BOT_TOKEN: str = Field(
        description="Discord token to connect the bot client",
    )
    DISCORD_GUILD_ID: str = Field(
        description="Guild ID to sync slash commands",
    )


config = Config()
