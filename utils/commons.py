import json
import os
from utils.logger import log


def save_json_file(data, fname="test.json", dirname="test_jsons"):
    """
    Saves a dictionary or list to a JSON file.

    Args:
        data (dict or list): The Python object to save.
        filepath (str): The path to the output file (e.g., 'data/output.json').
    """
    try:

        filepath = os.path.join(
            dirname, fname + ".json" if ".json" not in fname.lower() else fname
        )
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as json_file:
            json.dump(data, json_file, indent=4, ensure_ascii=False)

        log.debug(f"Successfully saved data to {filepath}")

    except TypeError as e:
        log.error(f"Error: The data is not JSON serializable. {e}")
    except IOError as e:
        log.error(f"Error: Could not write to file {filepath}. {e}")
    except Exception as e:
        log.error(f"An unexpected error occurred: {e}")
