# src/tasks.py

from crewai import Task



class ResearchTasks:

    def research_task(self, agent, topic):
        return Task(
            description=f"Gather comprehensive, citable information on '{topic}'.",
            expected_output="Complete raw text including facts, statistics, and citations.",
            agent=agent
        )

    def analysis_task(self, agent, context):
        return Task(
            description="Query the internal knowledge base using the retrieval tool and synthesize insights into an outline.",
            expected_output="Structured outline with key themes and thesis statements.",
            agent=agent,
            context=context
        )

    def reporting_task(self, agent, context, output_file="final_report.md"):
        return Task(
            description=f"Draft a professional Markdown report based on analysis, saving to '{output_file}'.",
            expected_output="Final polished research report, confirmed saved.",
            agent=agent,
            context=context,
            output_file=output_file
        )

    def verification_task(self, agent, context):
        return Task(
            description="Verify 3-5 key claims using the citation tool and provide a short verification report.",
            expected_output="Short verification report for each claim.",
            agent=agent,
            context=context
        )
