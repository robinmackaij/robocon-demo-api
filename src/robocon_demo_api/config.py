from pathlib import Path


class _Config:
    def __init__(self):
        self.api_key = "100101011101010101101101"
        self.portraits_path = Path(".") / "portraits"
        if not self.portraits_path.exists():
            self.portraits_path.mkdir()


CONFIG = _Config()
