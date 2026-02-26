import os
from crewai import Agent, Task, Crew, Process, LLM


def create_financial_analysis_crew(document_text):

    llm = LLM(
        model="openai/gpt-4o-mini",
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPENROUTER_API_KEY"),
        temperature=0
    )

    financial_analyst = Agent(
        role="Senior Financial Intelligence Analyst",
        goal="Extract structured financial insights from any financial document",
        backstory="""
        Expert in analyzing earnings reports, 10-K, 10-Q,
        balance sheets, investor presentations, and financial summaries.
        """,
        verbose=True,
        allow_delegation=False,
        llm=llm
    )

    task = Task(
        description=f"""
        Analyze the financial document carefully.

        Extract:

        - Document type
        - Reporting period
        - Revenue
        - Gross Profit
        - Operating Income
        - Net Income
        - EPS
        - Operating Margin
        - Free Cash Flow
        - Total Assets
        - Total Liabilities
        - Cash Position
        - YoY Changes
        - Business Segments
        - Risks

        If a metric is missing, return null.

        Return STRICT JSON format:

        {{
            "document_type": "",
            "period": "",
            "summary": "",
            "financials": {{
                "revenue": null,
                "gross_profit": null,
                "operating_income": null,
                "net_income": null,
                "eps": null,
                "operating_margin": null,
                "free_cash_flow": null,
                "total_assets": null,
                "total_liabilities": null,
                "cash": null
            }},
            "yoy_changes": [],
            "business_segments": [],
            "risks": []
        }}

        Document:
        {document_text}
        """,
        expected_output="Structured JSON containing financial insights.",
        agent=financial_analyst
    )

    crew = Crew(
        agents=[financial_analyst],
        tasks=[task],
        process=Process.sequential,
        verbose=True
    )

    return crew