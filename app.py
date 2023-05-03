from flask import Flask, render_template, request, jsonify
from main import analyze_article, answer_question, get_llm
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    article_url = data.get('article_url')
    api_key = data.get('api_key')

    if article_url and api_key:
        try:
            title, source, date, author, analysis, doc = analyze_article(article_url, api_key)
            result = {
                'title': title,
                'source': source,
                'date': str(date),
                'author': author,
                'analysis': analysis
            }
            return jsonify(result)
        except Exception as e:
            return jsonify({"error": str(e)})
    else:
        return jsonify({"error": "Please enter a URL and an API key."})

@app.route('/ask_question', methods=['POST'])
def ask_question():
    data = request.get_json()
    question = data.get('question')
    doc_text = data.get('doc_text')
    api_key = data.get('api_key')

    if not question or not doc_text or not api_key:
        return jsonify({"error": "Please provide a question, the document text, and an API key."})

    try:
        answer = answer_question(question, doc_text, api_key)
        return jsonify({"answer": answer})
    except Exception as e:
        print(e)  # Log the error for debugging
        return jsonify({"error": "An error occurred while processing the question."})

if __name__ == '__main__':
    app.run(debug=True)
