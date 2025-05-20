from APIs.claude import call_claude
from APIs.deepseek import call_deepseek
from APIs.gemini import call_gemini
from APIs.llama import call_llama
from APIs.openai import call_openai
from APIs.qwen import call_qwen


def testing_apis():
    text = "Hi!"

    # # Test OpenAI
    # print("🌍 Testing OpenAI...")
    # openai_response = call_openai([{"role": "user", "content": text}])
    # print("OpenAI Response:", openai_response)

    ## Test DeepSeek
    # print("🌍 Testing DeepSeek...")
    # deepseek_response = call_deepseek([{"role": "user", "content": text}])
    # print("DeepSeek Response:", deepseek_response)

    # #Test Gemini
    # print("🌍 Testing Gemini...")
    # gemini_response = call_gemini(text)
    # print("Gemini Response:", gemini_response)

    # #Test LLaMA
    # print("🌍 Testing LLaMA...")
    # llama_response = call_llama(text)
    # print("LLaMA Response:", llama_response)

    # #Test Claude
    # print("🌍 Testing Claude...")
    # claude_response = call_claude(text)
    # print("Claude Response:", claude_response)

    # #Test Qwen (Not Yet Available)
    # print("🌍 Testing Qwen...")
    # qwen_response = call_qwen(text)
    # print("Qwen Response:", qwen_response)

    print("✅ All API tests completed.")