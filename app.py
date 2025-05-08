from flask import Flask, render_template, request, jsonify
import requests
import xml.etree.ElementTree as ET
import re
import time
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import string

nltk.download('stopwords')



app = Flask(__name__)

def preprocess(text):
    stemmer = PorterStemmer()
    stop_words = set(stopwords.words('english'))
    tokens = re.findall(r'\b\w+\b', text.lower())
    filtered = [stemmer.stem(word) for word in tokens if word not in stop_words and word not in string.punctuation]
    return ' '.join(filtered)

def fetch_arxiv_papers(query, max_results=10):
    """
    Fetch papers from arXiv API based on search query
    """
    # Format query for arXiv API
    formatted_query = '+AND+'.join(query.split())
    base_url = f"http://export.arxiv.org/api/query?search_query=all:{formatted_query}&start=0&max_results={max_results}"
    
    try:
        # Make API request
        response = requests.get(base_url)
        response.raise_for_status()
        
        # Parse XML response
        root = ET.fromstring(response.content)
        
        # Define namespace
        namespace = {'atom': 'http://www.w3.org/2005/Atom'}
        
        papers = []
        for entry in root.findall('.//atom:entry', namespace):
            # Extract paper information
            title = entry.find('./atom:title', namespace).text.strip().replace('\n', ' ')
            summary = entry.find('./atom:summary', namespace).text.strip().replace('\n', ' ')
            
            # Truncate summary if it's too long
            if len(summary) > 300:
                summary = summary[:300] + "..."
            
            # Extract authors
            authors = []
            for author in entry.findall('./atom:author/atom:name', namespace):
                authors.append(author.text.strip())
            
            # Extract date and convert to year
            published = entry.find('./atom:published', namespace).text
            year = published.split('-')[0]
            
            # Extract URL
            url = entry.find('./atom:id', namespace).text
            
            # Create paper object
            paper = {
                "title": title,
                "summary": summary,
                "authors": ", ".join(authors),
                "year": year,
                "url": url
            }
            
            papers.append(paper)
        
        return papers
        
    except Exception as e:
        print(f"Error fetching papers from arXiv: {e}")
        return []
def rank_papers_by_similarity(papers, query):
    # Combine query and all summaries for vectorization
    texts = [preprocess(query)] + [preprocess(paper["summary"]) for paper in papers]

    
    # Convert text to TF-IDF vectors
    vectorizer = TfidfVectorizer().fit_transform(texts)
    
    # Compute cosine similarity of query with each paper summary
    cosine_similarities = cosine_similarity(vectorizer[0:1], vectorizer[1:]).flatten()
    
    # Attach score and sort
    for i, score in enumerate(cosine_similarities):
        papers[i]["score"] = score
    ranked_papers = sorted(papers, key=lambda x: x["score"], reverse=True)
    
    return ranked_papers


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search')
def search():
    query = request.args.get('q', '')
    
    if not query:
        return jsonify({"papers": []})
    
    # Fetch papers from arXiv
   
    papers = fetch_arxiv_papers(query)
    papers = rank_papers_by_similarity(papers, query)

    
    return jsonify({"papers": papers})

if __name__ == '__main__':
    app.run(debug=True)