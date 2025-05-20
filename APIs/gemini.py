import requests
import json
import logging
from config import gemini_api_key

# ✅ Updated API URL with correct version and model
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1/models/gemini-1.5-pro:generateContent"

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def call_gemini(prompt, temperature=0.7, max_tokens=500):
    """
    Calls the Gemini API to generate text.

    Args:
        prompt (str): The user input prompt.
        temperature (float): Sampling temperature (default: 0.7).
        max_tokens (int): Maximum response length (default: 500).

    Returns:
        str: AI-generated response or error message.
    """
    if not prompt:
        return "Error: Prompt cannot be empty."

    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": temperature,
            "maxOutputTokens": max_tokens
        }
    }

    try:
        logging.info(f"🛠️ Sending request to Gemini API: {json.dumps(payload, indent=2)}")

        response = requests.post(
            GEMINI_API_URL,
            headers=headers,
            params={"key": gemini_api_key},
            json=payload
        )
        response.raise_for_status()  # Raise an exception for HTTP errors

        # ✅ Debugging: Print the raw API response
        logging.info(f"🔄 Gemini API Response Status Code: {response.status_code}")
        logging.info(f"🔄 Gemini API Response Content: {response.text}")

        response_data = response.json()

        # ✅ Extract AI response safely
        if "candidates" in response_data and len(response_data["candidates"]) > 0:
            if "content" in response_data["candidates"][0]:
                if "parts" in response_data["candidates"][0]["content"]:
                    ai_response = response_data["candidates"][0]["content"]["parts"][0]["text"].strip()
                    logging.info(f"✅ Extracted Gemini Response: {ai_response}")
                    return ai_response
                else:
                    return "Error: 'parts' field missing in Gemini API response."
            else:
                return "Error: 'content' field missing in Gemini API response."
        else:
            return "Error: 'candidates' field missing or empty in Gemini API response."

    except requests.exceptions.RequestException as e:
        if hasattr(e, 'response') and e.response is not None:
            logging.error(f"❌ Gemini API Error Status Code: {e.response.status_code}")
            logging.error(f"❌ Gemini API Error Content: {e.response.text}")
            return f"Error: {e} - {e.response.text}"
        return f"Error: {e}"

    except ValueError as e:
        return f"Error: Invalid JSON response from Gemini API - {e}"

    except KeyError as e:
        return f"Error: Invalid response format from Gemini API - {e}"