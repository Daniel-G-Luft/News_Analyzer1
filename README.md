
# News_Analyzer

This web application allows users to analyze articles by providing a concise summary and ask follow-up questions about the analyzed content. It uses OpenAI's GPT-3 model to generate the summaries and answer the questions. The application is built with Flask, JavaScript, and the OpenAI API.

## Features

- Analyze articles from any URL
- Summarize articles using OpenAI's GPT-3
- Ask follow-up questions about the analyzed content
- Get answers to your questions powered by GPT-3

## Installation

1. Clone the repository:

    git clone https://github.com/your_username/ArticleAnalyzer.git


2. Install the required Python packages:

    pip install -r requirements.txt

3. You will need to get an OpenAI API Key:

    To get an OpenAI API Key please go to the OpenAI website: https://openai.com/blog/openai-api

## Usage

1. Run the Flask app:

    python app.py

2. Visit 'http:127.0.0.1:5000' in your web browswer to access the web application.

3. Enter an article URL and click the "Analyze" button to get a summary of the article. 

4. After the summary appears, you can ask follow-up questions about the analyzed content by typing your question and clicking "Ask" button.  

## Dependencies 

- Flask
- Newspaper3k
- OpenAI
- Langchain

## Contributing 

As an entry-level programmer, I am open to any feedback and suggestions. Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.
