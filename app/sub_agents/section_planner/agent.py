"""Section Planner agent definition."""

from google.adk.agents import LlmAgent

from app.config import config
from .prompt import SECTION_PLANNER_PROMPT


section_planner = LlmAgent(
    model=config.worker_model,
    name="section_planner",
    description="Breaks down the research plan into a structured markdown outline of report sections.",
    instruction=SECTION_PLANNER_PROMPT,
    output_key="report_sections",
)