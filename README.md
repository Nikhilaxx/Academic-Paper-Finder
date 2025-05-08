# 🧠 Intelligent Research Paper Search Engine

This project is a **Flask-based web application** that enables intelligent search of research papers using the [arXiv API](https://arxiv.org/help/api). It preprocesses search queries and paper summaries, ranks results using **TF-IDF** and **cosine similarity**, and displays the most relevant papers to the user.

---

## 🚀 Features

- 🔍 Fetches real-time research papers from arXiv based on user queries
- 🧹 Text preprocessing: lowercasing, tokenization, stopword removal, stemming
- 📊 Semantic ranking using TF-IDF + cosine similarity
- 🌐 Simple frontend with search functionality using AJAX
- 📄 Displays titles, authors, summaries, years, and direct links to arXiv

---

## 🧱 Tech Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML, JavaScript (AJAX), Jinja2
- **ML/NLP**: NLTK, Scikit-learn (TF-IDF, Cosine Similarity)
- **API**: arXiv Open API (XML format)

---

## 📦 Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/ir-research-paper-search.git
   cd ir-research-paper-search
   ```

2. **Create and activate a virtual environment (optional but recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the app**
   ```bash
   python app.py
   ```

5. **Open your browser and visit**
   ```
   http://127.0.0.1:5000
   ```

---

## 📂 Project Structure

```
├── app.py                # Main Flask application
├── templates/
│   └── index.html        # Frontend search interface
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation
```

---

## ✨ Example

* **Query**: `"transformer models in NLP"`
* **Top Result**: Paper titled *"Attention Is All You Need"* with summary, authors, and arXiv link.

---


## 📘 License

This project is licensed under the MIT License. See `LICENSE` for more details.

---

## 🤝 Acknowledgements

* arXiv API
* NLTK
* Scikit-learn
