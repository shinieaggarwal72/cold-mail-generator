# AI Cold Mail Generator

An AI-powered Cold Email Generator that automatically extracts job postings from a company’s career page text and writes personalized business outreach emails, using LangChain, GROQ, and Streamlit.

<br>

### ![View Live](https://cold-mail-generator-shinie.streamlit.app/)

<br>

## Interface
![Interface](./demo/im1.png)

## Features

- Job Extraction – Uses Llama-3 via GROQ to parse raw career page text into structured job postings (role, experience, skills, and description).
- Cold Email Generation – Generates highly relevant emails tailored to each job.
- Portfolio Matching – Integrates with a ChromaDB vector store to showcase your most relevant past projects.
- Streamlit UI – Simple web interface that runs locally or on Streamlit Cloud.
- Secure Key Input – Users enter their own GROQ API key at runtime (never exposed or hardcoded).

<br>

## Tech Stack

- Frontend: Streamlit
- LLM API: LangChain + GROQ (llama-3.3-70b-versatile)
- Vector Store: ChromaDB (persistent local DB)
- Language: Python 3.10+
- Data: resources/my_portfolio.csv for your project portfolio

<br>

## Usage Guide

- Enter your GROQ API Key when prompted.
- Paste a career-page job text or job description in the input box.
- (Optional) The app automatically queries your project portfolio (my_portfolio.csv) to find the most relevant examples.
- Click “Generate Cold Email” and wait a few seconds.
- The AI-generated email appears below — ready to copy and send!

<br>

## Installation (locally)
```bash

# 1. Clone the repo
git clone https://github.com/shinieaggarwal72/cold-mail-generator.git
cd cold-mail-generator/app

# 2. Create a virtual environment
python -m venv mailenv
source mailenv/bin/activate   # On Windows: mailenv\Scripts\activate

# 3. Install dependencies
pip install -r ../requirements.txt

# 4. Run the Streamlit app
streamlit run app.py
```







