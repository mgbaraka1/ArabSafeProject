from openai import OpenAI
from config import openai_api_key
import logging

# Initialize OpenAI client
client = OpenAI(api_key=openai_api_key)

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def call_openai(messages, model="gpt-3.5-turbo", max_tokens=500, temperature=0.7):
    if not messages:
        logging.error("❌ Error: Messages cannot be empty.")
        return None  # Return None if messages list is empty

    try:
        # Format messages correctly
        formatted_messages = [{"role": msg["role"], "content": msg["content"]} for msg in messages]

        logging.info(f"🛠️ Sending request to OpenAI API with messages: {formatted_messages}")

        # Make the API call
        response = client.chat.completions.create(
            model=model,
            messages=formatted_messages,
            max_tokens=max_tokens,
            temperature=temperature
        )

        logging.info(f"🔄 Raw API Response Type: {type(response)} | Content: {response}")

        # ✅ Correctly extract message content
        if response.choices and len(response.choices) > 0:
            first_choice = response.choices[0]  # Choice object
            content = first_choice.message.content.strip() if first_choice.message.content else None

            if content:
                logging.info(f"✅ Extracted Content: {content}")
                return content
            else:
                logging.error("❌ Content extraction failed: No message content found.")
                return None
        else:
            logging.error("❌ Invalid response structure: No choices found.")
            return None

    except TypeError as te:
        logging.error(f"❌ TypeError during API call: {str(te)}")
        return None
    except KeyError as ke:
        logging.error(f"❌ KeyError during API call: {str(ke)}")
        return None
    except Exception as e:
        logging.error(f"❌ General Exception during API call: {str(e)}")
        return None  # Return None to indicate a failure