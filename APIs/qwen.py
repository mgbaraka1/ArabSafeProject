import requests
from config import qwen_api_key

QWEN_API_URL = "https://dashscope.aliyuncs.com/api/v1/services/chat/completions"


def call_qwen(messages, model="qwen-turbo", max_tokens=500, temperature=0.7):
    if not messages:
        return "Error: Messages cannot be empty."

    headers = {
        "Authorization": f"Bearer {qwen_api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "model": model,
        "input": {
            "messages": messages
        },
        "parameters": {
            "max_tokens": max_tokens,
            "temperature": temperature,
            "result_format": "message"
        }
    }

    try:
        response = requests.post(QWEN_API_URL, headers=headers, json=data)
        response.raise_for_status()

        response_data = response.json()

        # Handle Qwen's specific response structure
        if response_data.get("output") and response_data["output"].get("choices"):
            return response_data["output"]["choices"][0]["message"]["content"].strip()
        else:
            return "Error: Unexpected response format"

    except requests.exceptions.RequestException as e:
        # Log the full error response for debugging
        if hasattr(e, 'response') and e.response is not None:
            try:
                error_details = e.response.json()
                return f"Error: {e} - {error_details}"
            except ValueError:
                return f"Error: {e} - Status code: {e.response.status_code}"
        return f"Error: {e}"
    except KeyError as e:
        return f"Error: Invalid response format from Qwen API - {e}"