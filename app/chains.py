from langchain_groq import ChatGroq
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.exceptions import OutputParserException


class Chain:
    def __init__(self, api_key: str):
        """Initialize the Chain with a user-provided API key."""
        if not api_key:
            raise ValueError("API key is required to initialize Chain.")
        
        self.llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            groq_api_key=api_key,
            temperature=0
        )

    def extract_jobs(self, cleaned_text: str):
        """Extract job information from scraped text."""
        prompt_extract = PromptTemplate.from_template(
            """
            ### SCRAPED TEXT FROM WEBSITE:
            {page_data}

            ### INSTRUCTION:
            The scraped text is from the career page of a website.
            Extract all job postings and return them in **valid JSON** format containing:
            'role', 'experience', 'skills', and 'description'.
            ### VALID JSON (NO PREAMBLE):
            """
        )

        chain_extract = prompt_extract | self.llm
        res = chain_extract.invoke(input={'page_data': cleaned_text})

        try:
            json_parser = JsonOutputParser()
            res = json_parser.parse(res.content)
        except OutputParserException:
            raise OutputParserException("Context too big or invalid JSON format.")
        
        return res if isinstance(res, list) else [res]

    def write_mail(self, job, links):
        """Generate a cold email for the extracted job."""
        prompt_email = PromptTemplate.from_template(
            """
            ### JOB DESCRIPTION:
            {job_description}

            ### INSTRUCTION:
            You are Shinie, a business development executive at XYZ. XYZ is an AI & Software Consulting company
            dedicated to facilitating seamless business automation through AI tools.
            You must write a professional cold email to the client based on the job above,
            highlighting XYZ’s capabilities in delivering tailored AI and software solutions.
            Include the most relevant portfolio links from: {link_list}
            Do not add a preamble or greeting header.
            ### EMAIL (NO PREAMBLE):
            """
        )

        chain_email = prompt_email | self.llm
        res = chain_email.invoke({"job_description": str(job), "link_list": links})
        return res.content
