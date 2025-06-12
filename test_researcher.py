from researcher_agent import ResearcherAgent
import json

def test_url(url, description):
    print(f"\n{'='*80}")
    print(f"Testing: {description}")
    print(f"URL: {url}")
    print('='*80)
    
    agent = ResearcherAgent()
    try:
        result = agent.extract_content(url)
        print(f"\nExtraction Method: {result['source']}")
        print("\nExtracted Content (first 500 characters):")
        print('-'*80)
        print(result['content'][:500] + "...")
        print('-'*80)
        print("\nContent Length:", len(result['content']), "characters")
        return True
    except Exception as e:
        print(f"\nError: {str(e)}")
        return False

def main():
    # Test cases
    test_cases = [
        {
            "url": "https://www.isna.ir/news/1402121412343/",
            "description": "Persian News Website (ISNA)"
        },
        {
            "url": "https://www.bbc.com/persian",
            "description": "Persian International News (BBC Persian)"
        },
        {
            "url": "https://www.theguardian.com/international",
            "description": "English News Website (The Guardian)"
        }
    ]
    
    successful_tests = 0
    total_tests = len(test_cases)
    
    for test in test_cases:
        if test_url(test["url"], test["description"]):
            successful_tests += 1
    
    print(f"\nTest Summary:")
    print(f"Successful Tests: {successful_tests}/{total_tests}")

if __name__ == "__main__":
    main() 