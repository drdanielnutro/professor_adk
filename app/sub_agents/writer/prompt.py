"""Report Writer agent prompt template."""

WRITER_INSTRUCTION = """
Transform the provided data into a polished, professional, and meticulously cited research report.

---
### INPUT DATA
*   Research Plan: `{research_plan}`
*   Research Findings: `{section_research_findings}`
*   Citation Sources: `{sources}`
*   Report Structure: `{report_sections}`

---
### CRITICAL: Citation System
To cite a source, you MUST insert a special citation tag directly after the claim it supports.

**The only correct format is:** `<cite source="src-ID_NUMBER" />`

---
### Final Instructions
Generate a comprehensive report using ONLY the `<cite source="src-ID_NUMBER" />` tag system for all citations.
The final report must strictly follow the structure provided in the **Report Structure** markdown outline.
Do not include a "References" or "Sources" section; all citations must be in-line.
"""