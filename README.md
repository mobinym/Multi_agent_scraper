# Website Content Summarizer

A modern, user-friendly desktop application that extracts and summarizes content from websites using AI. Built with PyQt5 and featuring a sleek dark theme interface.


## Features

- 🌐 Extract content from any website URL
- 📝 Clean and readable content extraction
- 🤖 AI-powered content summarization
- 🎨 Modern dark theme UI
- ⚡ Asynchronous processing with loading indicators
- 📱 Responsive and user-friendly interface
- 🔄 Real-time content updates
- 📋 Markdown support for summaries

## Requirements

- Python 3.8 or higher
- PyQt5
- Required Python packages (see requirements.txt)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/website-summarizer.git
cd website-summarizer
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the application:
```bash
python gui_app.py
```

2. Enter a website URL in the input field
3. Click "Summarize" or press Enter
4. Wait for the content to be processed
5. View the extracted content and summary in the respective panels

## Project Structure

```
website-summarizer/
├── gui_app.py              # Main GUI application
├── extract_and_summarize.py # Content extraction and summarization logic
├── researcher_agent.py     # Web content extraction module
├── summarizer_agent.py     # AI summarization module
├── requirements.txt        # Project dependencies
└── README.md              # This file
```

## Features in Detail

### Content Extraction
- Extracts main content from web pages
- Removes ads and unnecessary elements
- Preserves formatting and structure
- Handles various website layouts

### AI Summarization
- Generates concise summaries
- Maintains key information
- Supports multiple languages
- Markdown formatting for better readability

### User Interface
- Dark theme for reduced eye strain
- Split-pane view for content and summary
- Loading indicators for better UX
- Responsive layout
- Error handling with user-friendly messages

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- PyQt5 for the GUI framework
- BeautifulSoup4 for web scraping
- Newspaper3k for content extraction
- LangChain for AI processing
