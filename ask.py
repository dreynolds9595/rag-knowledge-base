from dotenv import load_dotenv
load_dotenv()

from app.pipeline import ask

if __name__ == "__main__":
    print("RAG Knowledge Base — type 'quit' to exit\n")
    while True:
        query = input("Ask a question: ").strip()
        if query.lower() in ("quit", "exit"):
            break
        if not query:
            continue

        result = ask(query)
        print("\n--- Answer ---")
        print(result["answer"])
        print("\n--- Sources ---")
        for s in result["sources"]:
            print(f"[{s['id']}] {s['source']}")
        print()