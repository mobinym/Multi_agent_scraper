from langchain.llms import Ollama
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import markdown
import re

class SummarizerAgent:
    def __init__(self):
        callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])
        self.llm = Ollama(
            model="llama3.2",
            temperature=0.7,
            callback_manager=callback_manager,
            verbose=True,
        )
        
        self.summary_prompt = PromptTemplate(
            input_variables=["content"],
            template="""
            Please analyze the following text and create a structured summary. If the text is in Persian, provide the summary in Persian. If the text is in English, provide the summary in English.

            Follow this exact structure:

            # [Main Title]
            [A comprehensive one-paragraph summary of the entire text]

            ## Key Points
            - [First key point]
            - [Second key point]
            - [Third key point]
            - [Fourth key point]
            - [Fifth key point]

            Original text:
            {content}

            Note: Ensure the summary maintains the original language of the text and follows the exact structure above.
            """
        )
        
        self.chain = LLMChain(llm=self.llm, prompt=self.summary_prompt)

    def clean_markdown(self, text):
        """Clean and format the markdown output"""
        text = re.sub(r'\n{3,}', '\n\n', text)
        text = re.sub(r'(#+)([^#\n])', r'\1 \2', text)
        text = re.sub(r'^\s*[-*]\s*', '- ', text, flags=re.MULTILINE)
        text = re.sub(r' +', ' ', text)
        return text.strip()

    def summarize(self, content):
        """Summarize the content using the LLM"""
        try:
            summary = self.chain.run(content)
            
            cleaned_summary = self.clean_markdown(summary)
            
            return cleaned_summary
        except Exception as e:
            raise Exception(f"خطا در خلاصه‌سازی: {str(e)}")

    def save_summary(self, summary, output_file="summary.md"):
        """Save the summary to a markdown file"""
        try:
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(summary)
            return True
        except Exception as e:
            raise Exception(f"خطا در ذخیره‌سازی خلاصه: {str(e)}")