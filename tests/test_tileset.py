"""Tests for tilesets"""
import importlib.util
import json
import os
from pathlib import Path

import pytest

from pytiled_parser import tileset

TESTS_DIR = Path(os.path.dirname(os.path.abspath(__file__)))
TEST_DATA = TESTS_DIR / "test_data"
TILE_SETS = TEST_DATA / "tilesets"


ALL_TILESET_DIRS = TILE_SETS.glob("*")


@pytest.mark.parametrize("tileset_dir", ALL_TILESET_DIRS)
def test_tilesets_integration(tileset_dir):
    """ This could be redundant, but it is useful just to ensure that anything in there
    is at least sanity checked"""
    # it's a PITA to import like this, don't do it
    # https://stackoverflow.com/a/67692/1342874
    spec = importlib.util.spec_from_file_location(
        "expected", tileset_dir / "expected.py"
    )
    expected = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(expected)

    raw_tileset_path = tileset_dir / "tileset.json"

    with open(raw_tileset_path) as raw_tileset:
        tileset_ = tileset.cast(json.loads(raw_tileset))

    assert tileset_ == expected.EXPECTED
