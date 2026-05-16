import importlib
import pkgutil
from pathlib import Path


def load_test_data():
    """Dynamically load all test data from test_data directory."""
    test_data = {}
    test_data_dir = Path(__file__).parent / "test_data"

    for module_info in pkgutil.iter_modules([str(test_data_dir)]):
        module = importlib.import_module(f"tests.test_data.{module_info.name}")
        key = getattr(module, "ISO_CODE", module_info.name)
        test_data[key] = module.TEST_DATA

    return test_data


ALL_TEST_DATA = load_test_data()
