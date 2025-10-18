import streamlit as st
from langchain_community.document_loaders import WebBaseLoader
from chains import Chain
from portfolio import Portfolio
from utils import clean_text

st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon="📧")

def create_streamlit_app(llm, portfolio, clean_text):
    
    url_input = st.text_input(
        "Enter a Job Page URL:",
        value='https://careers.walmart.com/us/jobs/WD2167847-senior-software-engineer'
    )

    if st.button("Submit"):
        try:
            from langchain_community.document_loaders import WebBaseLoader
            loader = WebBaseLoader(url_input)
            docs = loader.load()

            if not docs:
                st.error("Failed to fetch content. The page may be dynamic or blocked.")
                st.stop()

            data = clean_text(docs[0].page_content)
            portfolio.load_portfolio()

            jobs = llm.extract_jobs(data)
            for job in jobs:
                skills = job.get('skills', [])
                links = portfolio.query_links(skills)
                email = llm.write_mail(job, links)
                st.code(email, language='markdown')

        except Exception as e:
            st.error(f"Error: {e}")

if __name__ == "__main__":
    st.title("Cold Email Generator")
    api_key = st.text_input("🔑 Enter your GROQ API Key:", type="password")
    portfolio = Portfolio()

    if api_key:
        try:
            chain = Chain(api_key)
            st.success("✅ API key accepted. Enter job link below.")
            create_streamlit_app(chain, portfolio, clean_text)
        except Exception as e:
            st.error(f"Initialization Error: {e}")
    else:
        st.warning("Please enter your API key to continue.")
