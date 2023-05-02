from flask import Flask, render_template, request, jsonify
from main import analyze_article, answer_question, custom_prompt, llm
import openai

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    article_url = request.form.get('article_url')
    if article_url:
        try:
            title, source, date, author, analysis, doc = analyze_article(article_url, custom_prompt)
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
        return jsonify({"error": "Please enter a URL."})

@app.route('/ask_question', methods=['POST'])
def ask_question():
    question = request.form.get('question')
    doc_text = request.form.get('doc_text')

    if not question or not doc_text:
        return jsonify({"error": "Please provide a question and the document text."})

    try:
        # Combine the document text and the question
        prompt = f"{doc_text}\n\nQuestion: {question}\nAnswer:"

        # Use the OpenAI API to get the answer
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=100,
            n=1,
            stop=None,
            temperature=0.5,
        )

        answer = response.choices[0].text.strip()
        return jsonify({"answer": answer})
    except Exception as e:
        print(e)  # Log the error for debugging
        return jsonify({"error": "An error occurred while processing the question."})

if __name__ == '__main__':
    app.run(debug=True)