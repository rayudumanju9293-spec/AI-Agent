from langchain_community.tools import WikipediaQueryRun
from ddgs import DDGS
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_core.tools import Tool
from datetime import datetime

def save_to_txt(data: str, filename: str = "research_output.txt"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_text = f"--- Research Output ---\nTimestamp: {timestamp}\n\n{data}\n\n"

    with open(filename, "a", encoding="utf-8") as f:
        f.write(formatted_text)
    
    return f"Data successfully saved to {filename}"

save_tool = Tool(
    name="save_text_to_file",
    func=save_to_txt,
    description="Saves structured research data to a text file.",
)

def web_search(query: str) -> str:
    results = DDGS().text(query, max_results=5)

    if not results:
        return "No search results found."

    output = []

    for result in results:
        output.append(
            f"Title: {result.get('title', '')}\n"
            f"URL: {result.get('href', '')}\n"
            f"Description: {result.get('body', '')}"
        )

    return "\n\n".join(output)


search_tool = Tool(
    name="search",
    func=web_search,
    description="Search the web for current information. Use this when the user asks for information that may require web research.",
)

api_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=100)
wiki_tool = WikipediaQueryRun(api_wrapper=api_wrapper)