import os

from discord import Intents
from discord.ext.commands import Bot as DiscordBot

from config.config import Config
from utils.validator import is_valid_cog_filename


class Bot(DiscordBot):
    def __init__(
        self,
        *,
        config: Config = None,
        intents: Intents = None,
    ):
        if config is None:
            raise ValueError("Cannot instance the bot without a config")

        if intents is None:
            intents = Intents.default()

        self._config = config

        super().__init__(
            command_prefix="!",
            intents=intents,
        )

    @property
    def config(self):
        return self._config

    async def setup(self):
        await self._load_cogs()

        print("Setup complete")

    async def _load_cogs(self, dir: str = "cogs"):
        """Load all cogs from the specified directory."""

        loaded = 0
        failed = 0
        all_extension_paths = []

        for root, _, files in os.walk(dir):
            for filename in files:
                if is_valid_cog_filename(filename):
                    relative_path = os.path.relpath(
                        os.path.join(root, filename[:-3]), os.getcwd()
                    )
                    extension_path = relative_path.replace(os.sep, ".")
                    all_extension_paths.append(extension_path)

        len_files = len(all_extension_paths)
        print(f"Loading {len_files} cogs from {dir} (recursively)")

        for extension in all_extension_paths:
            try:
                await self.load_extension(extension)
                print(f"Successfully loaded extension {extension}")
                loaded += 1

            except Exception as e:  # noqa: BLE001
                print(f"Failed to load extension {extension}: -> {e!s}")
                failed += 1

        percent_loaded = loaded * 100 / len_files if len_files > 0 else 0

        print(
            f"Cogs loaded at {percent_loaded:.0f}% (t{len_files}/ l{loaded}/ f{failed})."
        )
