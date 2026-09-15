from asyncio import run

from classes.bot import Bot
from config.config import config


async def main(bot: Bot):
    await bot.setup()
    await bot.start(bot.config.DISCORD_BOT_TOKEN)


async def close(bot: Bot):
    await bot.close()


if __name__ == "__main__":
    bot = Bot(
        config=config,
    )

    try:
        run(main(bot))

    except KeyboardInterrupt:
        print("Program interrupted by user. Shutting bow gracefully")

    except Exception as e:  # noqa: BLE001
        print(f"Unexpected error in main program: -> {e}")

    finally:
        run(close(bot))
