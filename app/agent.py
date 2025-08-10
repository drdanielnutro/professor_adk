# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Main orchestration for the ADK Documentation Agent."""

import datetime
from google.adk.agents import LlmAgent, LoopAgent, SequentialAgent
from google.adk.tools.agent_tool import AgentTool

from .config import config
from .callbacks import citation_replacement_callback

# Import all subagents
from .sub_agents.planner import plan_generator
from .sub_agents.section_planner import section_planner
from .sub_agents.researcher import section_researcher
from .sub_agents.evaluator import research_evaluator
from .sub_agents.writer import report_composer
from .sub_agents.escalation import EscalationChecker
from .sub_agents.enhanced_search import enhanced_search_executor


# Research pipeline with iterative refinement
research_pipeline = SequentialAgent(
    name="research_pipeline",
    description="Executes a pre-approved research plan. It performs iterative research, evaluation, and composes a final, cited report.",
    sub_agents=[
        section_planner,
        section_researcher,
        LoopAgent(
            name="iterative_refinement_loop",
            max_iterations=config.max_search_iterations,
            sub_agents=[
                research_evaluator,
                EscalationChecker(name="escalation_checker"),
                enhanced_search_executor,
            ],
        ),
        report_composer,
    ],
)


# Main interactive planner agent
# NOTE: In ADK, context is automatically passed between agents through the framework.
# Sub-agents defined in the sub_agents list will receive the full conversation context
# without explicit parameter passing. Do NOT use transfer_to_agent() or similar functions.
interactive_planner_agent = LlmAgent(
    name="adk_interactive_planner",
    model=config.worker_model,
    description="ADK documentation specialist that helps users find information in the official Google ADK docs.",
    instruction=f"""
    You are a friendly and helpful ADK documentation specialist focused exclusively on the official Google ADK documentation at google.github.io/adk-docs/.
    
    **CRITICAL RULE: Never answer a question directly or refuse a request.** Your one and only first step is to use the `adk_plan_generator` tool to propose a research plan for the user's ADK-related question.
    If the user asks about ADK concepts, agents, tools, or development, you MUST immediately call `adk_plan_generator` to create a plan to find the answer in the official docs.
    
    Your workflow is:
    1.  **Plan:** Use `adk_plan_generator` to create a draft plan focused on ADK documentation.
    2.  **Refine:** Incorporate user feedback until the plan is approved.
    3.  **Execute:** Once the user gives EXPLICIT approval (e.g., "looks good, run it"), simply confirm that you'll start the research using the approved plan. The `research_pipeline` will automatically receive the context and execute the plan.

    Current date: {datetime.datetime.now().strftime("%Y-%m-%d")}
    Remember: All research is conducted EXCLUSIVELY within the official ADK documentation. Do not perform any research yourself.
    """,
    sub_agents=[research_pipeline],
    tools=[AgentTool(plan_generator)],
    output_key="research_plan",
)


# Export the root agent
root_agent = interactive_planner_agent