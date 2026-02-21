import pytest


def pytest_configure(config):
    config.addinivalue_line("markers", "slow: marks tests as slow")


def pytest_addoption(parser):
    parser.addoption("--report", action="store_true", default=False)