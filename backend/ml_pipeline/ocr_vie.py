def process_pdf_doctr(filepath: str):
    """
    Uses DocTR for bounding-box OCR on visually rich legacy PDFs.
    """
    print(f"Processing OCR for {filepath} using DocTR...")
    # TODO: Implement DocTR OCR
    return []

def process_layoutlm_vie(ocr_results: list):
    """
    Passes OCR coordinates to LayoutLM for Visual Information Extraction (key-value pairs).
    """
    print("Extracting key-value pairs using LayoutLM...")
    # TODO: Implement LayoutLM integration
    return {}
