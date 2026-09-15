import pytest

from utils.validator import is_valid_cog_filename


class TestValidator:
    @pytest.mark.parametrize(
        "filename",
        ["events.py", "general.py", "foo_bar.py", "Cog2.py", "123.py"],
    )
    def test_accepts_valid_cog_filename(self, filename):
        assert is_valid_cog_filename(filename) is True

    @pytest.mark.parametrize(
        "filename",
        [
            "__init__.py",
            "__main__.py",
            "events",
            "events.txt",
            "events.py.bak",
            "folder/events.py",
            "",
            ".pyc",
        ],
    )
    def test_rejects_invalid_cog_filename(self, filename):
        assert is_valid_cog_filename(filename) is False
