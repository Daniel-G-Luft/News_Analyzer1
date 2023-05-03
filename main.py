import openai
from newspaper import Article
from langchain.docstore.document import Document


def get_llm(api_key: str):
    openai.api_key = api_key
    return openai


def analyze_article(article_url, api_key: str):
    llm = get_llm(api_key)

    article = Article(article_url)
    article.download()
    article.parse()
    text = article.text
    doc = Document(page_content=text, metadata={"url": article_url})

    prompt = f"You are SummaryGPT, a skilled summary writer that reads and interprets articles and provides summaries. Your task is to write a concise summary of approximately 500 words for the following text:\n\n{text}\n\nCONCISE SUMMARY:"

    response = llm.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=500,
        n=1,
        stop=None,
        temperature=0.5,
    )

    summary = response.choices[0].text.strip()

    title = article.title
    source = article.source_url
    date = article.publish_date
    author = ", ".join(article.authors)

    return title, source, date, author, summary, doc


def answer_question(question: str, doc_text: str, api_key: str):
    llm = get_llm(api_key)

    prompt = f"{doc_text}\n\nQuestion: {question}\nAnswer:"

    response = llm.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.5,
    )

    answer = response.choices[0].text.strip()
    return answer
