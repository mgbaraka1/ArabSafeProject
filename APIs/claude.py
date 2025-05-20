import requests
from config import claude_api_key

claude_api_url = "https://api.anthropic.com/v1/messages"

def call_claude(message_content, model="claude-3-haiku-20240307", max_tokens=500, temperature=0.7):
    if not message_content:
        return "Error: Message content cannot be empty."

    if not claude_api_key:
        return "Error: API key is missing. Please check your config.py file."

    # Debug: Print the API key to verify it's correct (remove in production)
    print(f"Using API Key: {claude_api_key}")

    headers = {
        "anthropic-version": "2023-06-01",
        "x-api-key": claude_api_key,
        "content-type": "application/json"
    }

    data = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": message_content
            }
        ],
        "max_tokens": max_tokens,
        "temperature": temperature
    }

    try:
        response = requests.post(claude_api_url, headers=headers, json=data)
        response.raise_for_status()

        response_data = response.json()

        # The response format has changed in the new API
        if "content" in response_data and len(response_data["content"]) > 0:
            return response_data["content"][0]["text"]
        else:
            return "Error: Unexpected response format from Claude API"

    except requests.exceptions.HTTPError as e:
        # Log the full error response for debugging
        if e.response is not None:
            error_details = e.response.json()
            return f"HTTP Error: {e} - {error_details}"
        return f"HTTP Error: {e}"
    except requests.exceptions.RequestException as e:
        return f"Request Error: {e}"
    except KeyError as e:
        return f"Error: Invalid response format from Claude API - {e}"
    except Exception as e:
        return f"Unexpected Error: {e}"

# Example usage:
if __name__ == "__main__":
    test_message = "Hello, how are you?"
    response = call_claude(test_message)
    print(f"Claude Response: {response}")