"""
Generic config variables
"""

from pathlib import Path

PROJECT_FOLDER = Path(__file__).parent.resolve()

OUTPUT_FOLDER = PROJECT_FOLDER / "output"
OUTPUT_FOLDER.mkdir(exist_ok=True)
