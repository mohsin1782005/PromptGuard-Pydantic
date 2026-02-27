import json
from pydantic import ValidationError
from models import AIPromptRequest

def process_and_save(data: dict):
    try:
        # Validate the data
        request = AIPromptRequest(**data)
        print(f"SUCCESS: Data for User {request.user.user_id} is valid.")

        # Convert to a Dictionary
        # Here We using .model_dump() to get a clean Python dict
        final_data = request.model_dump()
        # Add the computed field manually to the dict if you want it in the file
        final_data["complexity_score"] = request.complexity

        # SAVE TO FILE
        filename = "sanitized_request.json"
        with open(filename, "w") as f:
            json.dump(final_data, f, indent=4)
        
        print(f"Created file: {filename}")

    except ValidationError as e:
        print(f"ERROR: {e.json()}")

if __name__ == "__main__":
    raw_input = {
        "user": {"u_id": 101, "tier": "premium"},
        "prompt": "Analyze the sales data for the last quarter using Python.",
        "model_name": "gemini-1.5-pro",
        "is_private": False
    }

    process_and_save(raw_input)