import openai
from newspaper import Article
from langchain import OpenAI, PromptTemplate
from langchain.docstore.document import Document
from langchain.chains.summarize import load_summarize_chain
from langchain.chains.question_answering import load_qa_chain

# Replace 'your_openai_api_key' with your actual OpenAI API key
openai_api_key = 'key here'

custom_prompt_template = "You are SummaryGPT, a skilled summary writer that reads and interprets articles and provides summaries. Your task is to write a concise summary of approximately 500 words for the following text:\n\n{text}\n\nCONCISE SUMMARY:"
custom_prompt = PromptTemplate(template=custom_prompt_template, input_variables=["text"])

llm = OpenAI(openai_api_key=openai_api_key, temperature=1)

def analyze_article(article_url, custom_prompt: PromptTemplate):
    article = Article(article_url)
    article.download()
    article.parse()
    text = article.text
    doc = Document(page_content=text, metadata={"url": article_url})

    chain = load_summarize_chain(
        llm,
        chain_type="map_reduce",
        map_prompt=custom_prompt,
        combine_prompt=custom_prompt
    )
    summary = chain.run([doc])

    title = article.title
    source = article.source_url
    date = article.publish_date
    author = ", ".join(article.authors)

    return title, source, date, author, summary, doc

def answer_question(question: str, input_documents, llm):
    chain = load_qa_chain(llm, chain_type="map_reduce")
    answer = chain.run(input_documents=input_documents, question=question)
    return answer

def fetch_and_analyze_article():
    global doc
    input_text = topic_entry.get()
    if input_text:
        status_label.config(text="Fetching and analyzing article...")
        root.update_idletasks()

        try:
            title, source, date, author, analysis, doc = analyze_article(input_text, custom_prompt)
            analysis_text.delete("1.0", tk.END)
            analysis_text.insert(tk.END, f"Title: {title}\nSource: {source}\nDate: {date}\nAuthor(s): {author}\n\nAnalysis: {analysis}\n")
            status_label.config(text="Article analyzed. You can ask follow-up questions.")
        except Exception as e:
            status_label.config(text="")
            messagebox.showerror("Error", f"An error occurred while fetching or analyzing the article: {e}")
    else:
        messagebox.showerror("Error", "Please enter a URL.")

def ask_question():
    global doc
    question = question_entry.get()
    if question:
        answer = answer_question(question, [doc], llm)
        analysis_text.insert(tk.END, f"\nQuestion: {question}\nAnswer: {answer}\n")
    else:
        messagebox.showerror("Error", "Please enter a question.")