"""Tests for JSONConverter class."""

import pytest
import json
import tempfile
import os
from pathlib import Path
from JSON2CSVLIB import JSONConverter
from JSON2CSVLIB.exceptions import ConversionError, ValidationError


class TestJSONConverter:
    """Test suite for JSONConverter class."""
    
    @pytest.fixture
    def converter(self):
        """Create a JSONConverter instance for testing."""
        return JSONConverter()
    
    @pytest.fixture
    def sample_data(self):
        """Sample JSON data for testing."""
        return [
            {"name": "John", "age": 30, "city": "NYC"},
            {"name": "Jane", "age": 25, "city": "LA"},
            {"name": "Bob", "age": 35, "city": "Chicago"}
        ]
    
    @pytest.fixture
    def nested_data(self):
        """Sample nested JSON data for testing."""
        return [
            {
                "user": {
                    "name": "John",
                    "age": 30,
                    "address": {
                        "city": "NYC",
                        "country": "USA"
                    }
                }
            },
            {
                "user": {
                    "name": "Jane",
                    "age": 25,
                    "address": {
                        "city": "LA",
                        "country": "USA"
                    }
                }
            }
        ]
    
    def test_simple_conversion(self, converter, sample_data):
        """Test basic JSON to CSV conversion."""
        result = converter.convert_to_csv(data=sample_data)
        
        assert "name" in result
        assert "age" in result
        assert "city" in result
        assert "John" in result
        assert "30" in result
        assert "NYC" in result
    
    def test_conversion_to_file(self, converter, sample_data):
        """Test conversion with output file."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as f:
            output_file = f.name
        
        try:
            converter.convert_to_csv(data=sample_data, output_file=output_file)
            
            assert os.path.exists(output_file)
            
            with open(output_file, 'r') as f:
                content = f.read()
                assert "name" in content
                assert "John" in content
        finally:
            if os.path.exists(output_file):
                os.remove(output_file)
    
    def test_nested_json_conversion(self, converter, nested_data):
        """Test conversion of nested JSON structures."""
        result = converter.convert_to_csv(data=nested_data, flatten_nested=True)
        
        assert "user.name" in result
        assert "user.age" in result
        assert "user.address.city" in result
        assert "user.address.country" in result
    
    def test_custom_delimiter(self, converter, sample_data):
        """Test conversion with custom delimiter."""
        result = converter.convert_to_csv(data=sample_data, delimiter=';')
        
        assert ';' in result
        lines = result.split('\n')
        assert lines[0].count(';') >= 2  # Header should have delimiters
    
    def test_single_dict_conversion(self, converter):
        """Test conversion of single dictionary."""
        data = {"name": "John", "age": 30}
        result = converter.convert_to_csv(data=data)
        
        assert "name" in result
        assert "John" in result
    
    def test_include_index(self, converter, sample_data):
        """Test conversion with row index."""
        result = converter.convert_to_csv(data=sample_data, include_index=True)
        
        assert "index" in result
        assert "0" in result
        assert "1" in result
    
    def test_custom_headers(self, converter, sample_data):
        """Test conversion with custom headers."""
        custom_headers = ["full_name", "years", "location"]
        
        # Note: This requires the data keys to match or mapping logic
        # For this test, we'll just verify the headers appear
        data = [
            {"full_name": "John", "years": 30, "location": "NYC"},
            {"full_name": "Jane", "years": 25, "location": "LA"}
        ]
        
        result = converter.convert_to_csv(
            data=data,
            custom_headers=custom_headers
        )
        
        assert "full_name" in result
        assert "years" in result
        assert "location" in result
    
    def test_load_json_file(self, converter):
        """Test loading JSON from file."""
        data = [{"name": "John", "age": 30}]
        
        with tempfile.NamedTemporaryFile(
            mode='w', 
            delete=False, 
            suffix='.json'
        ) as f:
            json.dump(data, f)
            json_file = f.name
        
        try:
            loaded_data = converter.load_json_file(file_path=json_file)
            assert loaded_data == data
        finally:
            if os.path.exists(json_file):
                os.remove(json_file)
    
    def test_preview_conversion(self, converter):
        """Test preview functionality."""
        data = [{"name": f"Person{i}", "age": 20 + i} for i in range(10)]
        
        preview = converter.preview_conversion(data=data, rows=3)
        
        # Should only contain 3 data rows plus header
        lines = preview.strip().split('\n')
        assert len(lines) == 4  # 1 header + 3 data rows
    
    def test_batch_conversion(self, converter):
        """Test batch file conversion."""
        # Create temporary JSON files
        temp_files = []
        output_dir = tempfile.mkdtemp()
        
        try:
            for i in range(3):
                data = [{"id": i, "name": f"Item{i}"}]
                with tempfile.NamedTemporaryFile(
                    mode='w',
                    delete=False,
                    suffix='.json',
                    dir=output_dir
                ) as f:
                    json.dump(data, f)
                    temp_files.append(f.name)
            
            converter.convert_batch(
                input_files=temp_files,
                output_dir=output_dir,
                flatten_nested=True
            )
            
            # Check that CSV files were created
            csv_files = list(Path(output_dir).glob("*.csv"))
            assert len(csv_files) == 3
            
        finally:
            # Cleanup
            for f in temp_files:
                if os.path.exists(f):
                    os.remove(f)
            for csv_file in Path(output_dir).glob("*.csv"):
                csv_file.unlink()
            os.rmdir(output_dir)
    
    def test_validation_enabled(self):
        """Test with validation enabled."""
        converter = JSONConverter(validate=True)
        
        invalid_data = "not a list"
        
        with pytest.raises(ValidationError):
            converter.convert_to_csv(data=invalid_data)
    
    def test_empty_data(self, converter):
        """Test conversion with empty data."""
        with pytest.raises(ValidationError):
            converter.convert_to_csv(data=[])
    
    def test_encoding_support(self, converter):
        """Test different file encodings."""
        data = [{"name": "José", "city": "São Paulo"}]
        
        with tempfile.NamedTemporaryFile(
            mode='w',
            delete=False,
            suffix='.csv',
            encoding='utf-8'
        ) as f:
            output_file = f.name
        
        try:
            converter.convert_to_csv(
                data=data,
                output_file=output_file,
                encoding='utf-8'
            )
            
            with open(output_file, 'r', encoding='utf-8') as f:
                content = f.read()
                assert "José" in content
                assert "São Paulo" in content
        finally:
            if os.path.exists(output_file):
                os.remove(output_file)


class TestEdgeCases:
    """Test edge cases and error handling."""
    
    def test_missing_keys(self):
        """Test data with inconsistent keys."""
        converter = JSONConverter(validate=False)
        data = [
            {"name": "John", "age": 30},
            {"name": "Jane"},  # Missing 'age'
            {"age": 35}  # Missing 'name'
        ]
        
        result = converter.convert_to_csv(data=data)
        assert result is not None
    
    def test_none_values(self):
        """Test handling of None values."""
        converter = JSONConverter()
        data = [
            {"name": "John", "age": None},
            {"name": None, "age": 30}
        ]
        
        result = converter.convert_to_csv(data=data)
        assert result is not None
    
    def test_special_characters(self):
        """Test handling of special characters."""
        converter = JSONConverter()
        data = [
            {"name": "John,Doe", "description": "Quote\"test"},
            {"name": "Jane\nSmith", "description": "Tab\ttest"}
        ]
        
        result = converter.convert_to_csv(data=data)
        assert result is not None
    
    def test_large_dataset(self):
        """Test with large dataset."""
        converter = JSONConverter()
        data = [{"id": i, "value": f"item_{i}"} for i in range(1000)]
        
        result = converter.convert_to_csv(data=data)
        lines = result.strip().split('\n')
        assert len(lines) == 1001  # 1 header + 1000 data rows
