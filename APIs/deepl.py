import httpx
from config import deepl_api_key

def translate_by_deepl(text, target_language="AR"):
    ##URL = "https://api-free.deepl.com/v2/translate" #For Free Version only
    URL = "https://api.deepl.com/v2/translate" #For Paid Version only

    try:
        response = httpx.post(
            URL,
            data={
                "auth_key": deepl_api_key,
                "text": text,
                "target_lang": target_language,
            },
        )
        response.raise_for_status()
        data = response.json()
        return data["translations"][0]["text"]
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 401:
            print("Invalid API key. Please check your credentials.")
        elif e.response.status_code == 429:
            print("Rate limit exceeded. Please wait and try again.")
        else:
            print(f"HTTP error occurred: {e}")
    except Exception as e:
        print(f"Error during deepl translation: {e}")
        return None