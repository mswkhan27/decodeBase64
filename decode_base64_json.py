import json
import base64
import re

# Function to decode base64, clean special characters, and replace null values
def process_json(input_file, output_file):
    with open(input_file, 'r') as file:
        data = json.load(file)

    def decode_and_clean(obj):
        if isinstance(obj, dict):
            return {k: decode_and_clean(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [decode_and_clean(v) for v in obj]
        elif isinstance(obj, str):
            try:
                # Attempt to decode base64 and clean special characters
                decoded = base64.b64decode(obj).decode('utf-8')
                cleaned = re.sub(r'[^\x20-\x7E]', '', decoded)
                return cleaned if cleaned else '-'
            except (base64.binascii.Error, UnicodeDecodeError):
                return obj
        elif obj is None:
            return '-'
        return obj

    cleaned_data = decode_and_clean(data)

    with open(output_file, 'w') as file:
        json.dump(cleaned_data, file, indent=4)

    print(f"Processed JSON saved to '{output_file}'")

# Example usage
process_json('sampleFile.json', '33output.json')