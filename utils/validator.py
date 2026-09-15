import re


def is_valid_cog_filename(filename: str) -> bool:
    """Checks if a filename is a valid cog file based on its naming convention."""

    return re.match(r"^(?!__)[a-zA-Z0-9_]*(?!__)\.py$", filename) is not None
