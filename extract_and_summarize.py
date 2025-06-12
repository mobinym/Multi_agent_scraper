from researcher_agent import ResearcherAgent
from summarizer_agent import SummarizerAgent

def extract_and_summarize(url):
    researcher = ResearcherAgent()
    summarizer = SummarizerAgent()

    try:
        result = researcher.extract_content(url)
        content = result['content']
        summary = summarizer.summarize(content)
        return content, summary
    except Exception as e:
        raise Exception(f"Error processing URL: {str(e)}")

if __name__ == "__main__":
    url = input("لطفا URL را وارد کنید: ")
    print(f"\nتست URL: {url}")
    content, summary = extract_and_summarize(url)
    print("\nContent:", content)
    print("\nSummary:", summary)