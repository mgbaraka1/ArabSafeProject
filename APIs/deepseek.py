import requests
from config import deepseek_api_key

DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"

def call_deepseek(messages, model="deepseek-chat", max_tokens=500, temperature=0.7):
    if not messages:
        return "Error: Messages cannot be empty."

    headers = {
        "Authorization": f"Bearer {deepseek_api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "model": model,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": temperature
    }

    try:
        response = requests.post(DEEPSEEK_API_URL, headers=headers, json=data)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Log the raw response for debugging
        print("DeepSeek API Response Status Code:", response.status_code)
        print("DeepSeek API Response Content:", response.text)

        response_data = response.json()
        return response_data["choices"][0]["message"]["content"].strip()
    except requests.exceptions.RequestException as e:
        # Log the full error response for debugging
        if hasattr(e, 'response') and e.response is not None:
            print("DeepSeek API Error Response Status Code:", e.response.status_code)
            print("DeepSeek API Error Response Content:", e.response.text)
            return f"Error: {e} - {e.response.text}"
        return f"Error: {e}"
    except KeyError as e:
        return f"Error: Invalid response format from DeepSeek API - {e}"
    except ValueError as e:
        # Handle JSON decode errors
        return f"Error: Invalid JSON response from DeepSeek API - {e}"