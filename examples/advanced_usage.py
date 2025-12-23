"""
Advanced usage examples for JSON2CSVLIB library.

This file demonstrates complex use cases and advanced features.
"""

from JSON2CSVLIB import JSONConverter, DataValidator, flatten_json
from JSON2CSVLIB.exceptions import ValidationError, ConversionError
import json


def example_1_batch_conversion():
    """Convert multiple JSON files at once."""
    print("=" * 50)
    print("Example 1: Batch Conversion")
    print("=" * 50)
    
    # Create sample JSON files
    datasets = {
        "sales_q1.json": [
            {"month": "Jan", "revenue": 10000, "expenses": 5000},
            {"month": "Feb", "revenue": 12000, "expenses": 5500},
            {"month": "Mar", "revenue": 15000, "expenses": 6000}
        ],
        "sales_q2.json": [
            {"month": "Apr", "revenue": 13000, "expenses": 5800},
            {"month": "May", "revenue": 14000, "expenses": 6200},
            {"month": "Jun", "revenue": 16000, "expenses": 6500}
        ],
        "sales_q3.json": [
            {"month": "Jul", "revenue": 17000, "expenses": 7000},
            {"month": "Aug", "revenue": 18000, "expenses": 7200},
            {"month": "Sep", "revenue": 19000, "expenses": 7500}
        ]
    }
    
    # Create files
    for filename, data in datasets.items():
        with open(filename, 'w') as f:
            json.dump(data, f)
    
    # Batch convert
    converter = JSONConverter()
    converter.convert_batch(
        input_files=list(datasets.keys()),
        output_dir="./csv_output/",
        flatten_nested=True,
        delimiter=','
    )
    
    print("✓ Converted 3 JSON files to CSV")
    print("✓ Output directory: ./csv_output/")


def example_2_data_validation():
    """Use data validation with strict mode."""
    print("\n" + "=" * 50)
    print("Example 2: Data Validation")
    print("=" * 50)
    
    # Valid data - consistent keys
    valid_data = [
        {"id": 1, "name": "John", "age": 30},
        {"id": 2, "name": "Jane", "age": 25},
        {"id": 3, "name": "Bob", "age": 35}
    ]
    
    # Invalid data - inconsistent keys
    invalid_data = [
        {"id": 1, "name": "John", "age": 30},
        {"id": 2, "name": "Jane", "email": "jane@email.com"},  # Different keys
    ]
    
    # Test with strict mode
    converter = JSONConverter(validate=True, strict_mode=True)
    
    try:
        print("Testing valid data...")
        result = converter.convert_to_csv(data=valid_data)
        print("✓ Valid data passed")
    except ValidationError as e:
        print(f"✗ Validation failed: {e}")
    
    try:
        print("\nTesting invalid data...")
        result = converter.convert_to_csv(data=invalid_data)
        print("✓ Data passed (shouldn't happen)")
    except ValidationError as e:
        print(f"✓ Validation correctly caught error: {e}")


def example_3_complex_nested_structure():
    """Handle complex nested JSON structures."""
    print("\n" + "=" * 50)
    print("Example 3: Complex Nested Structure")
    print("=" * 50)
    
    data = [
        {
            "user": {
                "id": 1,
                "profile": {
                    "name": "John Doe",
                    "contact": {
                        "email": "john@example.com",
                        "phone": {
                            "mobile": "555-0100",
                            "home": "555-0101"
                        }
                    }
                },
                "preferences": {
                    "notifications": True,
                    "theme": "dark"
                }
            },
            "metadata": {
                "created": "2024-01-01",
                "updated": "2024-12-22"
            }
        }
    ]
    
    converter = JSONConverter()
    
    # Flatten with custom separator
    csv_output = converter.convert_to_csv(
        data=data,
        flatten_nested=True,
        delimiter=','
    )
    
    print(csv_output)


def example_4_custom_flattening():
    """Use custom flattening with different separators."""
    print("\n" + "=" * 50)
    print("Example 4: Custom Flattening")
    print("=" * 50)
    
    nested_data = {
        "company": {
            "name": "TechCorp",
            "address": {
                "street": "123 Main St",
                "city": "NYC"
            }
        }
    }
    
    # Flatten with underscore separator
    flat_underscore = flatten_json(nested_data, separator="_")
    print("With underscore separator:")
    print(flat_underscore)
    
    # Flatten with dash separator
    flat_dash = flatten_json(nested_data, separator="-")
    print("\nWith dash separator:")
    print(flat_dash)
    
    # Flatten with custom max depth
    flat_limited = flatten_json(nested_data, max_depth=1)
    print("\nWith max depth = 1:")
    print(flat_limited)


def example_5_error_handling():
    """Demonstrate proper error handling."""
    print("\n" + "=" * 50)
    print("Example 5: Error Handling")
    print("=" * 50)
    
    converter = JSONConverter()
    
    # Test 1: Invalid file path
    try:
        print("Test 1: Non-existent file")
        converter.convert_to_csv(data="nonexistent.json")
    except Exception as e:
        print(f"✓ Caught error: {type(e).__name__}: {e}")
    
    # Test 2: Invalid data type
    try:
        print("\nTest 2: Invalid data type")
        converter.convert_to_csv(data="not a list or dict")
    except Exception as e:
        print(f"✓ Caught error: {type(e).__name__}: {e}")
    
    # Test 3: Empty data
    try:
        print("\nTest 3: Empty data")
        converter.convert_to_csv(data=[])
    except Exception as e:
        print(f"✓ Caught error: {type(e).__name__}: {e}")


def example_6_encoding_handling():
    """Handle different character encodings."""
    print("\n" + "=" * 50)
    print("Example 6: Encoding Handling")
    print("=" * 50)
    
    # Data with international characters
    data = [
        {"name": "José García", "city": "São Paulo", "country": "Brasil"},
        {"name": "François Müller", "city": "Zürich", "country": "Schweiz"},
        {"name": "Владимир", "city": "Москва", "country": "Россия"},
        {"name": "田中太郎", "city": "東京", "country": "日本"}
    ]
    
    converter = JSONConverter()
    
    # Save with UTF-8 encoding
    converter.convert_to_csv(
        data=data,
        output_file="international.csv",
        encoding='utf-8'
    )
    
    print("✓ Saved international characters with UTF-8 encoding")
    print("✓ File: international.csv")


def example_7_large_dataset_optimization():
    """Handle large datasets efficiently."""
    print("\n" + "=" * 50)
    print("Example 7: Large Dataset")
    print("=" * 50)
    
    import time