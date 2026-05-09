from huggingface_hub import InferenceClient
import os
from dotenv import load_dotenv

load_dotenv()
token = os.environ.get("HF_API_KEY")
client = InferenceClient(token=token)

text = "The patient was treated with Metformin for Type-2 Diabetes. Analysis showed mutations in the BRCA1 gene."
predictions = client.token_classification(text, model="d4data/biomedical-ner-all")
print(predictions)
