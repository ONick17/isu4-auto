import pytest
import os

try:
    from expertsystem.parser import parse
except ImportError:
    from .parser import parse


def test_parse():
    parse('/home/l140/education/data/expertsystem/forecast.csv')
