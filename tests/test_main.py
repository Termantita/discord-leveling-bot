from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

from main import close, main


class TestMain:
    @pytest.mark.asyncio
    async def test_starts_after_setup_with_configured_token(self):
        calls = []
        bot = SimpleNamespace(
            config=SimpleNamespace(DISCORD_BOT_TOKEN="test-token"),
            setup=AsyncMock(side_effect=lambda: calls.append("setup")),
            start=AsyncMock(side_effect=lambda token: calls.append(("start", token))),
        )

        await main(bot)

        assert calls == ["setup", ("start", "test-token")]
        bot.setup.assert_awaited_once_with()
        bot.start.assert_awaited_once_with("test-token")

    @pytest.mark.asyncio
    async def test_closes_the_bot(self):
        bot = SimpleNamespace(close=AsyncMock())

        await close(bot)

        bot.close.assert_awaited_once_with()
