from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

from cogs.events import Events
from cogs.general import General


class TestEvents:
    @pytest.mark.asyncio
    async def test_keeps_bot_and_reports_ready(self, capsys):
        bot = object()
        cog = Events(bot)

        await cog.on_ready()

        assert cog.bot is bot
        assert "Events cog is ready" in capsys.readouterr().out

    @pytest.mark.asyncio
    async def test_setup_adds_events_cog(self):
        bot = SimpleNamespace(add_cog=AsyncMock())

        await __import__("cogs.events", fromlist=["setup"]).setup(bot)

        added_cog = bot.add_cog.await_args.args[0]
        assert isinstance(added_cog, Events)
        assert added_cog.bot is bot


class TestGeneral:
    @pytest.mark.asyncio
    async def test_ping_sends_latency_embed(self):
        response = SimpleNamespace(send_message=AsyncMock())
        interaction = SimpleNamespace(
            client=SimpleNamespace(latency=0.1234),
            response=response,
        )
        cog = General(object())

        await General.ping.callback(cog, interaction)

        response.send_message.assert_awaited_once()
        embed = response.send_message.await_args.kwargs["embed"]
        assert embed.title == "🏓 Pong!"
        assert embed.fields[0].value == "123ms"

    @pytest.mark.asyncio
    async def test_setup_adds_general_cog(self):
        bot = SimpleNamespace(add_cog=AsyncMock())

        await __import__("cogs.general", fromlist=["setup"]).setup(bot)

        added_cog = bot.add_cog.await_args.args[0]
        assert isinstance(added_cog, General)
        assert added_cog.bot is bot
