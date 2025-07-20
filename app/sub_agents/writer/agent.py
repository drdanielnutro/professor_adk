"""Report Writer agent definition."""

from google.adk.agents import LlmAgent

from app.callbacks.research_callbacks import citation_replacement_callback
from app.config import config
from .prompt import WRITER_INSTRUCTION


report_composer = LlmAgent(
    model=config.critic_model,
    name="report_composer_with_citations",
    include_contents="none",
    description="Transforms research data and a markdown outline into a final, cited report.",
    instruction=WRITER_INSTRUCTION,
    output_key="final_cited_report",
    after_agent_callback=citation_replacement_callback,
)