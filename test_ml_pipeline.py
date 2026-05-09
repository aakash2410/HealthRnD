import sys
from backend.ml_pipeline.ner_linker import run_bern2_ner, link_to_umls_drugbank
from backend.ml_pipeline.ocr_vie import process_pdf_doctr, process_layoutlm_vie

def test_nlp_pipeline():
    print("=== Testing NLP Pipeline (Text NER) ===")
    
    # 1. Provide mock abstract (representing Layer 1 PubMed ingestion)
    sample_text = "The patient was treated with Metformin for Type-2 Diabetes. Analysis showed mutations in the BRCA1 gene."
    print(f"Input Text: '{sample_text}'")
    
    try:
        # 2. Run NER
        entities = run_bern2_ner(sample_text)
        print("\nExtracted Entities via Hugging Face API:")
        for e in entities:
            print(f"  - [{e['type']}] {e['entity']} (Confidence: {e['confidence']})")
            
        # 3. Link to UMLS/DrugBank
        linked_entities = link_to_umls_drugbank(entities)
        print("\nLinked Entities (Graph-Ready):")
        for e in linked_entities:
            print(f"  - {e['entity']} -> UMLS: {e.get('umls_id')}, DrugBank: {e.get('drugbank_id')}")
            
    except Exception as e:
        print(f"NLP Pipeline Error: {e}")

def test_ocr_vie_pipeline():
    print("\n=== Testing OCR/VIE Pipeline (PDF Processing) ===")
    
    try:
        # 1. OCR.space Extraction (Mock file path)
        print("Sending sample image to OCR.space API...")
        ocr_text = process_pdf_doctr("dummy_cdsco_document.pdf")
        
        # Print a snippet of the OCR text
        print(f"\nExtracted OCR Text snippet:\n{ocr_text[:100]}...\n")
        
        # 2. Hugging Face QA for Visual Information Extraction
        print("Sending OCR text to Hugging Face QA API for VIE...")
        structured_data = process_layoutlm_vie(ocr_text)
        
        print("\nFinal VIE Extracted JSON:")
        for k, v in structured_data.items():
            print(f"  - {k}: {v}")
            
    except Exception as e:
        print(f"OCR/VIE Pipeline Error: {e}")

if __name__ == "__main__":
    print("Starting ML Pipeline Integration Tests...\n")
    test_nlp_pipeline()
    test_ocr_vie_pipeline()
    print("\nML Pipeline Tests Completed.")
