"""add src to sys path so can find imports to unit tests"""
import sys
sys.path.append("./src")


def pytest_runtest_setup(item):
    """dummy function to add before tests"""
    # called for running each test in 'a' directory
    print("setting up", item)
