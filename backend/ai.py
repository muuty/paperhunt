import base64
import re

import google.generativeai as genai
import httpx

from backend.entity import Summary

SUMMARY_PROMPT = """
        Please summarize the following three points from the text:

        1) The research questions
        2) The main contributions
        3) The experimental setup and baselines

        Use this bullet structure:

        1. Research questions
        - {short keyword}: ...
        - (Add more bullets if needed)

        2. Main contributions
        - {short keyword}: ...
        - (Add more bullets if needed)

        3. Experimental setup and baselines
        - {short keyword}: ...
        - (Add more bullets if needed)

        Instructions:
        - Format your response using **plain text only**. Do not use markdown symbols like `**` (bold) or `*` (italics).
        - Begin each bullet with a short keyword followed by a colon (e.g., "Focus:", "Goal:", "Method:").
        - Omit references like "the paper" or "the authors"; use direct, concise statements.
        - Keep each point short and to the point.
"""


class GeminiAI:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    def summarize(self, pdf_url: str) -> Summary:
        doc_data = base64.standard_b64encode(httpx.get(pdf_url).content).decode("utf-8")
        response = self.model.generate_content(
            [{"mime_type": "application/pdf", "data": doc_data}, SUMMARY_PROMPT]
        )
        summary_text = response.text

        research_questions_pattern = (
            r"(?s)1\. Research questions(.*?)(?=2\. Main contributions|$)"
        )
        contributions_pattern = (
            r"(?s)2\. Main contributions(.*?)(?=3\. Experimental setup and baselines|$)"
        )
        experiments_pattern = r"(?s)3\. Experimental setup and baselines(.*)$"

        research_questions_text = self._extract(
            research_questions_pattern, summary_text
        )
        contributions_text = self._extract(contributions_pattern, summary_text)
        experiments_text = self._extract(experiments_pattern, summary_text)

        return Summary(research_questions_text, contributions_text, experiments_text)

    def _extract(self, pattern: str, text: str) -> str:
        match = re.search(pattern, text)
        if match:
            return match.group(1).strip()
        return ""
