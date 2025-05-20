import time
import requests
from config import llama_api_key

LLAMA_API_URL = "https://api.llama-api.com/chat/completions"

def call_llama(messages, model="llama3.3-70b", max_tokens=500, temperature=0.7, retries=3, delay=5):
    if isinstance(messages, str):
        messages = [{"role": "user", "content": messages}]
    elif not isinstance(messages, list):
        return "Error: Messages must be a list or a string."

    if not messages:
        return "Error: Messages cannot be empty."

    headers = {
        "Authorization": f"Bearer {llama_api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "model": model,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": temperature
    }

    for attempt in range(retries):
        try:
            print(f"Attempt {attempt + 1} of {retries}...")
            response = requests.post(LLAMA_API_URL, headers=headers, json=data)
            response.raise_for_status()

            print("Llama API Response Status Code:", response.status_code)
            print("Llama API Response Content:", response.text)

            response_data = response.json()

            # Handle the response format
            if isinstance(response_data, list) and len(response_data) > 0:
                if "error" in response_data[0]:
                    return f"Error: {response_data[0]['error']}"
                else:
                    return "Error: Unexpected response format from Llama API."

            # Handle the expected response format
            if "choices" in response_data and len(response_data["choices"]) > 0:
                return response_data["choices"][0]["message"]["content"].strip()
            else:
                return "Error: No choices found in the response."

        except requests.exceptions.RequestException as e:
            if attempt < retries - 1:
                print(f"Attempt {attempt + 1} failed. Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                if hasattr(e, 'response') and e.response is not None:
                    print("Llama API Error Response Status Code:", e.response.status_code)
                    print("Llama API Error Response Content:", e.response.text)
                    return f"Error: {e} - {e.response.text}"
                return f"Error: {e}"

        except KeyError as e:
            return f"Error: Invalid response format from Llama API - {e}"

        except ValueError as e:
            return f"Error: Invalid JSON response from Llama API - {e}"

# Example usage:
if __name__ == "__main__":
    messages = [{"role": "user", "content": "Tell me about Saudi Arabia."}]
    response = call_llama(messages)
    print("Response:", response)