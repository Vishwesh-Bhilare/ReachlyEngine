from pathlib import Path
from typing import Union


def ensure_dir(path: Union[str, Path]) -> Path:
    """
    Ensure directory exists and return Path.
    """
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p


def write_text(path: Union[str, Path], content: str, encoding: str = "utf-8") -> Path:
    """
    Write text content to a file, ensuring parent directory exists.
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding=encoding)
    return path


def read_text(path: Union[str, Path], encoding: str = "utf-8") -> str:
    """
    Read text content from file.
    """
    return Path(path).read_text(encoding=encoding)

