"""Tests for JSONConverter class."""

import pytest
from json2csv_pro import JSONConverter
from json2csv_pro.exceptions import ConversionError


def test_simple_conversion():
    converter = JSONConverter()
    data = [{"name": "John", "age": 30}]
    result = converter.convert_to_csv(data=data)
    assert "name,age" in result
    assert "John,30" in result


def test_nested_conversion():
    converter = JSONConverter()
    data = [{"user": {"name": "John", "age": 30}}]
    result = converter.convert_to_csv(data=data, flatten_nested=True)
    assert "user.name" in result
