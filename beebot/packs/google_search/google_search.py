import os

from autopack import Pack
from langchain import GoogleSerperAPIWrapper
from pydantic import BaseModel, Field

PACK_DESCRIPTION = (
    "Search Google for websites matching a given query. Useful for when you need to answer questions "
    "about current events."
)


class GoogleSearchArgs(BaseModel):
    query: str = Field(..., description="The query string")


class GoogleSearch(Pack):
    name = "google_search"
    description = PACK_DESCRIPTION
    args_schema = GoogleSearchArgs
    categories = ["Web"]

    def _run(self, query: str) -> str:
        if not os.environ.get("SERPER_API_KEY"):
            return "Google Search is not supported as the SERPER_API_KEY environment variable is not set"
        try:
            return format_results(GoogleSerperAPIWrapper().results(query).get("organic", []))

        except Exception as e:
            return f"Error: {e}"

    async def _arun(self, query: str) -> str:
        if not os.environ.get("SERPER_API_KEY"):
            return "Google Search is not supported as the SERPER_API_KEY environment variable is not set"
        try:
            query_results = await GoogleSerperAPIWrapper().aresults(query)
            return format_results(query_results.get("organic", []))

        except Exception as e:
            return f"Error: {e}"


def format_results(results: list[dict[str, str]]) -> str:
    formatted_results = [
        f"{result.get('link')}: {result.get('snippet')}" for result in results
    ]
    return f"Your search results are: {' | '.join(formatted_results)}"
