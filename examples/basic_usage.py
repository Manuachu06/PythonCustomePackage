"""
Basic usage examples for JSON2CSVLIB library.

This file demonstrates simple, everyday use cases.
"""

from jsonutils import JSONConverter


def example_1_simple_conversion():
    """Convert a simple list of dictionaries to CSV."""
    print("=" * 50)
    print("Example 1: Simple Conversion")
    print("=" * 50)
    
    # Create converter
    converter = JSONConverter()
    
    # Sample data
    data = [
        {"name": "John Doe", "age": 30, "city": "New York"},
        {"name": "Jane Smith", "age": 25, "city": "Los Angeles"},
        {"name": "Bob Johnson", "age": 35, "city": "Chicago"}
    ]
    
    # Convert to CSV string
    csv_output = converter.convert_to_csv(data=data)
    print(csv_output)
    
    # Save to file
    converter.convert_to_csv(data=data, output_file="output.csv")
    print("\n✓ Saved to output.csv")


def example_2_nested_json():
    """Convert nested JSON structure to CSV."""
    print("\n" + "=" * 50)
    print("Example 2: Nested JSON")
    print("=" * 50)
    
    converter = JSONConverter()
    
    # Nested data
    data = [
        {
            "name": "John",
            "age": 30,
            "address": {
                "city": "NYC",
                "country": "USA"
            },
            "contacts": {
                "email": "john@email.com",
                "phone": "555-0100"
            }
        },
        {
            "name": "Jane",
            "age": 25,
            "address": {
                "city": "LA",
                "country": "USA"
            },
            "contacts": {
                "email": "jane@email.com",
                "phone": "555-0200"
            }
        }
    ]
    
    # Flatten and convert
    csv_output = converter.convert_to_csv(
        data=data,
        flatten_nested=True
    )
    print(csv_output)


def example_3_custom_delimiter():
    """Use custom delimiter (semicolon)."""
    print("\n" + "=" * 50)
    print("Example 3: Custom Delimiter")
    print("=" * 50)
    
    converter = JSONConverter()
    
    data = [
        {"product": "Laptop", "price": 999, "stock": 50},
        {"product": "Mouse", "price": 25, "stock": 200},
        {"product": "Keyboard", "price": 75, "stock": 150}
    ]
    
    # Use semicolon as delimiter
    csv_output = converter.convert_to_csv(
        data=data,
        delimiter=';'
    )
    print(csv_output)


def example_4_from_json_file():
    """Load JSON from file and convert."""
    print("\n" + "=" * 50)
    print("Example 4: From JSON File")
    print("=" * 50)
    
    import json
    
    # Create sample JSON file
    data = [
        {"id": 1, "name": "Product A", "price": 10.99},
        {"id": 2, "name": "Product B", "price": 15.99},
        {"id": 3, "name": "Product C", "price": 20.99}
    ]
    
    with open("sample_data.json", "w") as f:
        json.dump(data, f)
    
    # Convert from file
    converter = JSONConverter()
    converter.convert_to_csv(
        data="sample_data.json",
        output_file="output_from_file.csv"
    )
    print("✓ Converted sample_data.json to output_from_file.csv")


def example_5_with_index():
    """Include row index in output."""
    print("\n" + "=" * 50)
    print("Example 5: With Row Index")
    print("=" * 50)
    
    converter = JSONConverter()
    
    data = [
        {"task": "Task 1", "status": "Complete"},
        {"task": "Task 2", "status": "Pending"},
        {"task": "Task 3", "status": "In Progress"}
    ]
    
    csv_output = converter.convert_to_csv(
        data=data,
        include_index=True
    )
    print(csv_output)


def example_6_preview():
    """Preview first few rows before converting."""
    print("\n" + "=" * 50)
    print("Example 6: Preview Conversion")
    print("=" * 50)
    
    converter = JSONConverter()
    
    # Generate large dataset
    data = [
        {"id": i, "value": f"Item {i}", "price": i * 10}
        for i in range(100)
    ]
    
    # Preview first 5 rows
    preview = converter.preview_conversion(data=data, rows=5)
    print("Preview of first 5 rows:")
    print(preview)
    print(f"\n(Full dataset has {len(data)} rows)")


if __name__ == "__main__":
    # Run all examples
    example_1_simple_conversion()
    example_2_nested_json()
    example_3_custom_delimiter()
    example_4_from_json_file()
    example_5_with_index()
    example_6_preview()
    
    print("\n" + "=" * 50)
    print("All examples completed!")
    print("=" * 50)