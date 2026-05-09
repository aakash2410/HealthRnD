from huggingface_hub import InferenceClient
import os
from dotenv import load_dotenv

load_dotenv()
token = os.environ.get("HF_API_KEY")
client = InferenceClient(token=token)

models = [
    "Qwen/Qwen2.5-7B-Instruct",
    "meta-llama/Meta-Llama-3-8B-Instruct",
    "mistralai/Mixtral-8x7B-Instruct-v0.1",
    "google/gemma-7b-it"
]

for m in models:
    try:
        print(f"\nTesting {m}...")
        res = client.chat_completion(
            messages=[{"role": "user", "content": "Who founded RetinaAI Health?"}],
            model=m,
            max_tokens=20
        )
        print("Success:", res.choices[0].message.content)
        break
    except Exception as e:
        print("Error:", e)

