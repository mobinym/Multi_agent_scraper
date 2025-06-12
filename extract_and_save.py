from researcher_agent import ResearcherAgent
import sys

def test_url(url):
    output_file = "extracted_content.txt"
    agent = ResearcherAgent()

    try:
        result = agent.extract_content(url)
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(f"URL: {url}\n")
            f.write(f"Extraction Method: {result['source']}\n\n")
            # Write each sentence on a new line
            sentences = result['content'].split('. ')
            for sentence in sentences:
                if sentence.strip():
                    f.write(sentence.strip() + '.\n')
        print(f"محتوا با موفقیت استخراج و در فایل {output_file} ذخیره شد.")
    except ValueError as e:
        print(f"خطا: {str(e)}")
    except ConnectionError as e:
        print(f"خطا: {str(e)}")
    except TimeoutError as e:
        print(f"خطا: {str(e)}")
    except PermissionError as e:
        print(f"خطا: {str(e)}")
    except FileNotFoundError as e:
        print(f"خطا: {str(e)}")
    except Exception as e:
        print(f"خطا: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("لطفا URL را به عنوان آرگومان وارد کنید.")
        print("مثال: python extract_and_save.py https://example.com")
        sys.exit(1)
    
    url = sys.argv[1]
    print(f"\nتست URL: {url}")
    test_url(url)