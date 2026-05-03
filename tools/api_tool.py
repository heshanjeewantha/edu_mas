# tools/api_tool.py
"""
Wikipedia Topic Fetcher Tool — Student A's custom tool.

Calls the free Wikipedia public API
"""
import wikipediaapi
from crewai.tools import BaseTool
from pydantic import BaseModel, Field

from logger import log_tool_call, log_tool_result, log_error


class WikiInputSchema(BaseModel):
    """Input schema for the WikipediaTool."""
    topic: str = Field(
        ...,
        description="The educational topic to look up on Wikipedia (e.g. 'Photosynthesis')"
    )

class WikipediaTool(BaseTool):
    """
    Fetches a plain-language factual summary of an educational topic
    from Wikipedia's free public API.

    This tool is used by the Coordinator agent to build a grounded
    knowledge base before quiz generation begins.

    Args:
        topic (str): The educational topic to search on Wikipedia.

    Returns:
        str: A factual summary of up to 1000 characters, or an error message
             prefixed with 'ERROR:' if the topic cannot be found.
    """
    name: str = "wikipedia_topic_fetcher"
    description: str = (
        "Fetches a factual summary of any educational topic from Wikipedia. "
        "Use this to get accurate, grounded knowledge before generating questions. "
        "Input: a topic string. Output: a plain-text summary."
    )
    args_schema: type[BaseModel] = WikiInputSchema

    def _run(self, topic: str) -> str:
        log_tool_call("wikipedia_topic_fetcher", {"topic": topic})
        try:
            wiki = wikipediaapi.Wikipedia(
                language="en",
                user_agent="EduMAS/1.0 (educational multi-agent system)"
            )
            page = wiki.page(topic)
            if not page.exists():
                result = f"ERROR: Topic '{topic}' not found on Wikipedia. Try a more specific term."
                log_tool_result("wikipedia_topic_fetcher", result)
                return result
            summary = page.summary[:1000]
            log_tool_result("wikipedia_topic_fetcher", f"Fetched {len(summary)} chars for '{topic}'")
            return summary
        except Exception as e:
            error_msg = f"ERROR fetching Wikipedia data: {str(e)}"
            log_error("WikipediaTool", error_msg)
            return error_msg
