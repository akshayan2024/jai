"""Compatibility package providing the ``jai_api`` namespace."""
import importlib
import sys

# Import the existing 'api' package
_api = importlib.import_module('api')

# Expose the same package under the 'jai_api' namespace
sys.modules[__name__] = _api
sys.modules[__name__].__path__ = _api.__path__

# Map ``jai_api.constants`` to the root ``constants`` package used by tests
sys.modules[f'{__name__}.constants'] = importlib.import_module('constants')

