import sys
from backend.api.rag_engine import handle_rag_query

def run_rag_test():
    print("=== Testing RAG Engine Orchestration ===\n")
    
    # We will ask a complex cross-domain question
    query = "Who founded RetinaAI Health, and what patents do they hold?"
    print(f"User Query: '{query}'\n")
    
    try:
        response = handle_rag_query(query)
        
        if response.get("status") == "success":
            print("RAG Response Generated Successfully:\n")
            print("-" * 50)
            print(response.get("data"))
            print("-" * 50)
        else:
            print(f"RAG Failed: {response.get('message')}")
            
    except Exception as e:
        print(f"Test Execution Error: {e}")

if __name__ == "__main__":
    run_rag_test()
