"""Tests for DataValidator class."""

import pytest
from jsonutils import DataValidator
from jsonutils.exceptions import ValidationError


class TestDataValidator:
    """Test suite for DataValidator class."""
    
    @pytest.fixture
    def validator(self):
        """Create a DataValidator instance."""
        return DataValidator()
    
    def test_valid_data(self, validator):
        """Test validation of valid data."""
        data = [
            {"name": "John", "age": 30},
            {"name": "Jane", "age": 25}
        ]
        
        assert validator.validate_data(data=data) is True
    
    def test_empty_list(self, validator):
        """Test validation fails on empty list."""
        with pytest.raises(ValidationError, match="cannot be empty"):
            validator.validate_data(data=[])
    
    def test_not_a_list(self, validator):
        """Test validation fails when data is not a list."""
        with pytest.raises(ValidationError, match="must be a list"):
            validator.validate_data(data={"name": "John"})
    
    def test_non_dict_items(self, validator):
        """Test validation fails when items are not dictionaries."""
        with pytest.raises(ValidationError, match="must be dictionaries"):
            validator.validate_data(data=["string", "items"])
    
    def test_strict_mode_consistent_keys(self, validator):
        """Test strict mode with consistent keys."""
        data = [
            {"name": "John", "age": 30},
            {"name": "Jane", "age": 25}
        ]
        
        assert validator.validate_data(data=data, strict=True) is True
    
    def test_strict_mode_inconsistent_keys(self, validator):
        """Test strict mode fails with inconsistent keys."""
        data = [
            {"name": "John", "age": 30},
            {"name": "Jane", "city": "NYC"}  # Different keys
        ]
        
        with pytest.raises(ValidationError, match="different keys"):
            validator.validate_data(data=data, strict=True)
    
    def test_non_strict_mode_inconsistent_keys(self, validator):
        """Test non-strict mode allows inconsistent keys."""
        data = [
            {"name": "John", "age": 30},
            {"name": "Jane", "city": "NYC"}  # Different keys
        ]
        