from unittest.mock import AsyncMock

import pytest
from discord import Intents

from classes.bot import Bot
from config.config import Config


class TestBot:
    @staticmethod
    def make_config():
        return Config(
            DISCORD_BOT_TOKEN="token",
            DISCORD_GUILD_ID="guild",
            _env_file=None,
        )

    def test_requires_configuration(self):
        with pytest.raises(ValueError, match="without a config"):
            Bot()

    def test_exposes_configuration(self):
        settings = self.make_config()
        bot = Bot(config=settings)

        assert bot.config is settings

    def test_uses_default_intents(self, monkeypatch):
        expected_intents = Intents.none()
        default_intents = lambda: expected_intents
        monkeypatch.setattr("classes.bot.Intents.default", default_intents)

        bot = Bot(config=self.make_config())

        assert bot.intents.value == expected_intents.value

    def test_preserves_explicit_intents(self):
        expected_intents = Intents.all()

        bot = Bot(config=self.make_config(), intents=expected_intents)

        assert bot.intents.value == expected_intents.value

    @pytest.mark.asyncio
    async def test_setup_delegates_to_load_cogs(self, monkeypatch):
        bot = Bot(config=self.make_config())
        load_cogs = AsyncMock()
        monkeypatch.setattr(bot, "_load_cogs", load_cogs)

        await bot.setup()

        load_cogs.assert_awaited_once_with()

    @pytest.mark.asyncio
    async def test_loads_only_valid_cog_files(self, monkeypatch, capsys):
        bot = Bot(config=self.make_config())
        load_extension = AsyncMock()
        monkeypatch.setattr(bot, "load_extension", load_extension)
        monkeypatch.setattr(
            "classes.bot.os.walk",
            lambda directory: [
                (directory, [], ["events.py", "__init__.py", "notes.txt"])
            ],
        )
        monkeypatch.setattr("classes.bot.os.getcwd", lambda: ".")

        await bot._load_cogs("cogs")

        load_extension.assert_awaited_once_with("cogs.events")
        assert "Cogs loaded at 100%" in capsys.readouterr().out

    @pytest.mark.asyncio
    async def test_continues_after_an_extension_fails(self, monkeypatch, capsys):
        bot = Bot(config=self.make_config())
        load_extension = AsyncMock(side_effect=[RuntimeError("broken"), None])
        monkeypatch.setattr(bot, "load_extension", load_extension)
        monkeypatch.setattr(
            "classes.bot.os.walk",
            lambda directory: [(directory, [], ["first.py", "second.py"])],
        )
        monkeypatch.setattr("classes.bot.os.getcwd", lambda: ".")

        await bot._load_cogs()

        assert load_extension.await_count == 2
        assert "Cogs loaded at 50%" in capsys.readouterr().out

    @pytest.mark.asyncio
    async def test_handles_a_directory_without_cogs(self, monkeypatch, capsys):
        bot = Bot(config=self.make_config())
        load_extension = AsyncMock()
        monkeypatch.setattr(bot, "load_extension", load_extension)
        monkeypatch.setattr("classes.bot.os.walk", lambda directory: [])

        await bot._load_cogs()

        load_extension.assert_not_awaited()
        assert "Cogs loaded at 0%" in capsys.readouterr().out
