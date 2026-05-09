from huggingface_hub import InferenceClient
import os
from dotenv import load_dotenv

load_dotenv()
token = os.environ.get("HF_API_KEY")
client = InferenceClient(token=token)

text = "The patient was treated with Metformin for Type-2 Diabetes. Analysis showed mutations in the BRCA1 gene."
models = [
    "samrawal/bert-base-uncased_clinical-ner",
    "alvaroalon2/biobert_diseases_ner",
    "blaze999/Medical-NER"
]

for m in models:
    try:
        print(f"Testing {m}...")
        preds = client.token_classification(text, model=m)
        print("Success:", preds)
    except Exception as e:
        print("Error:", e)
