# allam.py
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

# Model setup
MODEL_NAME = "ALLaM-AI/ALLaM-7B-Instruct-preview"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME, torch_dtype=torch.bfloat16)

device = "cuda" if torch.cuda.is_available() else "cpu"
model = model.to(device)

# Set a default pad token if missing
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

def call_allam(messages: list) -> str:
    if not isinstance(messages, list) or not messages:
        raise ValueError("Input must be a non-empty list of message dictionaries.")

    # Extract the prompt from the first message
    prompt = messages[0].get("content", "").strip()
    if not prompt:
        raise ValueError("Message content cannot be empty.")

    # Force translation by making the prompt explicit
    translation_prompt = f"[Translate] {prompt} [/Translate]"

    # Tokenize and move to device
    inputs = tokenizer(translation_prompt, return_tensors="pt", return_token_type_ids=False).to(device)

    # Generate response
    with torch.no_grad():
        response = model.generate(
            **inputs,
            max_new_tokens=256,
            min_new_tokens=10,
            do_sample=True,
            top_k=50,
            top_p=0.95,
            temperature=0.7,
            eos_token_id=tokenizer.eos_token_id,
            pad_token_id=tokenizer.pad_token_id
        )

    # Decode response
    translated_text = tokenizer.batch_decode(response, skip_special_tokens=True)[0].strip()

    # Remove the prompt from the response if echoed
    if translated_text.startswith(translation_prompt):
        translated_text = translated_text[len(translation_prompt):].strip()

    # Filter out non-translation responses
    generic_responses = [
        "As an AI language model",  # Example: if the model starts with a disclaimer
        "Sorry, I can't",           # Example: if the model refuses the task
        "I am sorry",               # Example: polite rejection
    ]
    if any(phrase in translated_text for phrase in generic_responses):
        print("❌ Warning: Detected a generic or non-translation response.")
        return "[Error: Non-translation response detected]"

    # Log if response is empty
    if not translated_text:
        print("❌ Warning: Model returned an empty response.")
        return "[Error: Empty Response]"

    return translated_text