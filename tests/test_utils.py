"""Tests for utility functions."""

import pytest
from arcolabutils.utils import flatten_json, detect_delimiter


class TestFlattenJSON:
    """Test suite for flatten_json function."""
    
    def test_simple_flatten(self):
        """Test flattening simple nested structure."""
        data = {
            "user": {
                "name": "John",
                "age": 30
            }
        }
        
        result = flatten_json(data)
        
        assert result == {
            "user.name": "John",
            "user.age": 30
        }
    
    def test_deeply_nested_flatten(self):
        """Test flattening deeply nested structure."""
        data = {
            "user": {
                "profile": {
                    "name": "John",
                    "address": {
                        "city": "NYC"
                    }
                }
            }
        }
        
        result = flatten_json(data)
        
        assert result["user.profile.name"] == "John"
        assert result["user.profile.address.city"] == "NYC"
    
    def test_custom_separator(self):
        """Test flattening with custom separator."""
        data = {
            "user": {
                "name": "John"
            }
        }
        
        result = flatten_json(data, separator="_")
        
        assert "user_name" in result
        assert result["user_name"] == "John"
    
    def test_list_in_json(self):
        """Test flattening with lists."""
        data = {
            "user": {
                "name": "John",
                "hobbies": ["reading", "gaming"]
            }
        }
        
        result = flatten_json(data)
        
        assert "user.name" in result
        assert "user.hobbies" in result
        assert isinstance(result["user.hobbies"], str)
    
    def test_max_depth(self):
        """Test max depth limiting."""
        data = {
            "level1": {
                "level2": {
                    "level3": {
                        "level4": "deep"
                    }
                }
            }
        }
        
        result = flatten_json(data, max_depth=2)
        
        # Should stop flattening at depth 2
        assert "level1.level2" in result
    
    def test_empty_dict(self):
        """Test flattening empty dictionary."""
        result = flatten_json({})
        assert result == {}
    
    def test_no_nesting(self):
        """Test flattening flat dictionary."""
        data = {"name": "John", "age": 30}
        result = flatten_json(data)
        
        assert result == data


class TestDetectDelimiter:
    """Test suite for detect_delimiter function."""
    
    def test_comma_delimiter(self):
        """Test detection of comma delimiter."""
        sample = "name,age,city\nJohn,30,NYC"
        result = detect_delimiter(sample=sample)
        
        assert result == ','
    
    def test_semicolon_delimiter(self):
        """Test detection of semicolon delimiter."""
        sample = "name;age;city\nJohn;30;NYC"
        result = detect_delimiter(sample=sample)
        
        assert result == ';'
    
    def test_tab_delimiter(self):
        """Test detection of tab delimiter."""
        sample = "name\tage\tcity\nJohn\t30\tNYC"
        result = detect_delimiter(sample=sample)
        
        assert result == '\t'
    
    def test_pipe_delimiter(self):
        """Test detection of pipe delimiter."""
        sample = "name|age|city\nJohn|30|NYC"
        result = detect_delimiter(sample=sample)
        
        assert result == '|'
    
    def test_custom_candidates(self):
        """Test with custom delimiter candidates."""
        sample = "name:age:city"
        result = detect_delimiter(sample=sample, candidates=[',', ';', ':'])
        
        assert result == ':'
    
    def test_empty_sample(self):
        """Test with empty sample."""
        result = detect_delimiter(sample="")
        assert result == ','  # Default fallback
