import re
import json
import logging

def json_extractor(text: str):
    try:
        # Compile a regular expression pattern to match JSON objects
        json_pattern = re.compile(r'\{.*?\}', re.DOTALL)
        
        # Find all matches in the text
        json_matches = json_pattern.findall(text)

        # Initialize a list to hold the extracted JSON objects
        json_data = []

        # Parse each JSON section and add it to the list
        for match in json_matches:
            try:
                json_obj = json.loads(match)
                json_data.append(json_obj)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")
                logging.error(f"Error decoding JSON: {e}")

        # Return the last JSON object if the list is not empty
        if json_data:
            last_json_obj = json_data[-1]
            logging.info(f'Extracted JSON data: {last_json_obj}')
            return last_json_obj
        else:
            logging.info('No valid JSON data found')
            return None
    except Exception as e:
        logging.error(e)
        raise e  # Raise the exception without custom handling to avoid undefined variables

# Example usage:
input_text = '''
{"product_category": "hair care", "gender": "female", "price": 25, "product_description": "for dry hair, for dandruff problems"}
'''
output = json_extractor(input_text)
print(output)
