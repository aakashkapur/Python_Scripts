import json
import yaml
from typing import Any
import argparse

class FormatConverter:

    def __init__(self):
        self.supported_formats = ['json', 'yaml']

    def load_json(self, content: str) -> Any:
        try:
            return json.loads(content)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON: {e}")

    def load_yaml(self, content: str) -> Any:
        try:
            return yaml.safe_load(content)
        except yaml.YAMLError as e:
            raise ValueError(f"Invalid YAML: {e}")

    def convert(self, content: str, from_format: str, to_format: str) -> str:
        if from_format not in self.supported_formats:
            raise ValueError(f"Unsupported from_format: {from_format}")
        if to_format not in self.supported_formats:
            raise ValueError(f"Unsupported to_format: {to_format}")

        if from_format == 'json':
            data = self.load_json(content)
        elif from_format == 'yaml':
            data = self.load_yaml(content)

        if to_format == 'json':
            return json.dumps(data, indent=2)
        elif to_format == 'yaml':
            return yaml.safe_dump(data, default_flow_style=False)

if __name__ == "__main__":
    converter = FormatConverter()

    parser = argparse.ArgumentParser(description="Convert between JSON and YAML formats.")
    parser.add_argument("--from_format", choices=["json", "yaml"], help="The format to convert from.")
    parser.add_argument("--to_format", choices=["json", "yaml"], help="The format to convert to.")
    parser.add_argument("--from_file", help="The file containing the content to convert.")
    parser.add_argument("--to_file", help="The file to write the converted content to.")
    args = parser.parse_args()
    with open(args.from_file, 'r') as f:
        content = f.read()
    converted_content = converter.convert(content, args.from_format, args.to_format)
    with open(args.to_file, 'w') as f:
        f.write(converted_content)
        print(converted_content)
        print(f"Converted content written to {args.to_file}")
