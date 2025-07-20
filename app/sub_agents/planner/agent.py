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

"""Plan generator agent for creating ADK documentation research plans."""

from google.adk.agents import LlmAgent
from google.adk.tools import google_search

from ...config import config
from .prompt import get_plan_generator_prompt


plan_generator = LlmAgent(
    model=config.worker_model,
    name="adk_plan_generator",
    description="Generates research plans specifically for Google ADK documentation queries.",
    instruction=get_plan_generator_prompt(),
    tools=[google_search],
)