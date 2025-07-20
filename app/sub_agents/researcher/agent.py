"""Researcher agent definition."""

from google.adk.agents import LlmAgent
from google.adk.planners import BuiltInPlanner
from google.adk.tools import google_search
from google.genai import types as genai_types

from app.callbacks.research_callbacks import collect_research_sources_callback
from app.config import config
from .prompt import RESEARCHER_INSTRUCTION


section_researcher = LlmAgent(
    model=config.worker_model,
    name="adk_docs_researcher",
    description="Performs deep research exclusively within the official Google ADK documentation.",
    planner=BuiltInPlanner(
        thinking_config=genai_types.ThinkingConfig(include_thoughts=True)
    ),
    instruction=RESEARCHER_INSTRUCTION,
    tools=[google_search],
    output_key="section_research_findings",
    after_agent_callback=collect_research_sources_callback,
)