import pytest
from pydantic import ValidationError

from config.config import Config


class TestConfig:
    def test_builds_with_required_values(self):
        settings = Config(
            DISCORD_BOT_TOKEN="token",
            DISCORD_GUILD_ID="guild",
            _env_file=None,
        )

        assert settings.DISCORD_BOT_TOKEN == "token"
        assert settings.DISCORD_GUILD_ID == "guild"

    @pytest.mark.parametrize("missing_field", ["DISCORD_BOT_TOKEN", "DISCORD_GUILD_ID"])
    def test_requires_each_environment_value(self, monkeypatch, missing_field):
        monkeypatch.delenv("DISCORD_BOT_TOKEN", raising=False)
        monkeypatch.delenv("DISCORD_GUILD_ID", raising=False)
        values = {
            "DISCORD_BOT_TOKEN": "token",
            "DISCORD_GUILD_ID": "guild",
        }
        values.pop(missing_field)

        with pytest.raises(ValidationError):
            Config(_env_file=None, **values)

    def test_ignores_extra_values(self):
        settings = Config(
            DISCORD_BOT_TOKEN="token",
            DISCORD_GUILD_ID="guild",
            UNRELATED_VALUE="ignored",
            _env_file=None,
        )

        assert not hasattr(settings, "UNRELATED_VALUE")

    def test_ignores_empty_environment_values(self, monkeypatch):
        monkeypatch.setenv("DISCORD_BOT_TOKEN", "")
        monkeypatch.setenv("DISCORD_GUILD_ID", "guild")

        with pytest.raises(ValidationError):
            Config(_env_file=None)
