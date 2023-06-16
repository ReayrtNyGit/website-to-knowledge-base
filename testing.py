from typing import Optional

from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.document_loaders import UnstructuredURLLoader
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQAWithSourcesChain

import requests
import xml.etree.ElementTree as ET
from dotenv import load_dotenv
from loguru import logger
from knowledge_base import KnowledgeBase


load_dotenv()


def extract_urls_from_sitemap(sitemap):
    """
    Extract all URLs from a sitemap XML string.

    Args:
        sitemap_string (str): The sitemap XML string.

    Returns:
        A list of URLs extracted from the sitemap.
    """
    # Parse the XML from the string
    root = ET.fromstring(sitemap)

    # Define the namespace for the sitemap XML
    namespace = {"ns": "http://www.sitemaps.org/schemas/sitemap/0.9"}

    # Find all <loc> elements under the <url> elements
    urls = [
        url.find("ns:loc", namespace).text for url in root.findall("ns:url", namespace)
    ]

    # Return the list of URLs
    return urls

sitemap_url="https://nextjs.org/sitemap.xml"
pattern="api-refe"
sitemap = requests.get(sitemap_url).text
urls = extract_urls_from_sitemap(sitemap)
urls = [x for x in urls if pattern in x]
for url in urls:
    print(url)

# Build the knowledge base
# kb = KnowledgeBase(
#     sitemap_url="https://nextjs.org/sitemap.xml",
#     pattern="docs/api-refe",
#     chunk_size=8000,
#     chunk_overlap=3000,
# )