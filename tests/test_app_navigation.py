import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_nav_bar_exists_in_decor():
    assert (ROOT / "lib" / "decor.py").exists()
    spec = importlib.util.spec_from_file_location("lib.decor", ROOT / "lib" / "decor.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    assert hasattr(module, "nav_bar")


def test_single_xatbot_page_exists():
    assert (ROOT / "pages" / "1_xatbot.py").exists()
    assert not (ROOT / "pages" / "1_xat.py").exists()
