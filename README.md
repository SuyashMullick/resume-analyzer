# Resume Analyzer

An AI-powered tool that compares resumes against job descriptions and provides a match score along with improvement suggestions.

## Features

Upload a resume (PDF/DOCX) and a job description (text/PDF).

Get a match score that measures alignment.

See missing or underrepresented keywords.

Simple Gradio web interface for interaction.

## Tech Stack

Backend: FastAPI (Python)

AI/ML: Hugging Face Transformers, FAISS

UI: Gradio

Parsing: PyPDF2 / python-docx

## Setup

Clone the repository:

```
git clone https://github.com/yourusername/resume-analyzer.git
cd resume-analyzer
```

Create and activate a virtual environment:

```
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows
```

Install dependencies:
```
pip install -r requirements.txt
```

Note: You will need your own .env file with API keys and a dataset to run the project. These are not included in this repository.

## Running the App

Start the app locally:

```
python app.py
```

Then open the Gradio UI at http://127.0.0.1:7860
