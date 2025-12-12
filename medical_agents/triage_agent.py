import os
import json
from dotenv import load_dotenv
from typing import Literal, Tuple
import random
# import truststore  # SSL証明書エラーの対応のため

from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from openai import OpenAI
from agents import Agent, Runner, function_tool, SQLiteSession, set_trace_processors
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX
from braintrust import init_logger, load_prompt, wrap_openai
from braintrust.wrappers.openai import BraintrustTracingProcessor

from config import settings

load_dotenv()
# truststore.inject_into_ssl()

db = {
    "job_descriptions": {1: "I need an AI Engineer who knows langchain"},
    "state": {
        "session123": {
            "skills": [],
            "evaluation": [],  # list of typles (Skill, True/False), eg: [("Python", True)]
        }
    },
}

question_bank = {
    "python": {
        "easy": [
            "If `d` is a dictionary, then what does `d['name'] = 'Siddharta'` do?",
            "if `l1` is a list and `l2` is a list, then what is `l1 + l2`?",
        ],
        "medium": [
            "How do you remove a key from a dictionary?",
            "How do you reverse a list in python?",
        ],
        "hard": [
            "If `d` is a dictionary, then what does `d.get('name', 'unknown')` do?",
            "What is the name of the `@` operator (Example `a @ b`) in Python?",
        ],
    },
    "sql": {
        "easy": [
            "What does LIMIT 1 do at the end of a SQL statement?",
            "Explain this SQL: SELECT product_name FROM products WHERE cost < 500'",
        ],
        "medium": [
            "What is a view in SQL?",
            "How do we find the number of records in a table called `products`?",
        ],
        "hard": [
            "What is the difference between WHERE and HAVING in SQL?",
            "Name a window function in SQL",
        ],
    },
    "system design": {
        "easy": [
            "Give one reason where you would prefer a SQL database over a Vector database",
            "RAG requires a vector database. True or False?",
        ],
        "medium": [
            "Give one advantage and one disadvantage of chaining multiple prompts?",
            "Mention three reasons why we may not want to use the most powerful model?",
        ],
        "hard": [
            "Mention ways to speed up retrieval from a vector database",
            "Give an overview of Cost - Accuracy - Latency tradeoffs in an AI system",
        ],
    },
}


@function_tool
def extract_skills(session_id: str, job_id: int) -> list[str]:
    """
    This function takes session_id and job_id and returns a list of
    skills suitable for that job
    """
    print(">>> Tool called 'extract_skills':", session_id)
    db["state"][session_id]["skills"] = ["Python", "SQL", "System Design"]
    return ["Python", "SQL", "System Design"]


@function_tool
def update_evaluation(session_id: str, skill: str, evaluation_result: bool) -> bool:
    print(">>> Tool called 'update_evaluation':", session_id, skill, evaluation_result)
    db["state"][session_id]["evaluation"].append((skill, evaluation_result))
    return True


@function_tool
def get_next_skill_to_evaluate(session_id: str) -> str | None:
    print(">>> Tool called 'get_next_skill_to_evaluate':", session_id)
    all_skills = db["state"][session_id]["skills"]
    evaluated_skills = [
        skill for skill, evaluation in db["state"][session_id]["evaluation"]
    ]

    # for skill in all_skills:
    #     if skill not in evaluated_skills:
    #         return skill
    # return None

    remaining_skills = set(all_skills) - set(evaluated_skills)
    return remaining_skills.pop()


@function_tool
def get_question(topic: str, difficulty: Literal["easy", "medium", "hard"]) -> str:
    print(">>> Tool called 'get_question':", topic, difficulty)
    question = random.choice(question_bank[topic][difficulty])
    return question


TRIAGE_PROMPT = """
{RECOMMENDED_PROMPT_PREFIX}

You are an interview orchestrator. Your goal is to evaluate the candidate on the required skills.

# INSTRUCTIONS

Follow the following steps exactly

1. Extract key skills from the job description using extract_skills tool
2. Then welcome the candidate, explain the screening process and ask the candidate if they are ready 
3. Then, use the get_next_skill_to_evaluate tool to get the skill to evaluate
4. If the skill is not `None` then hand off to the "Skills Evaluator Agent" to perform the evaluation. Pass in the skill to evaluate
4. Once you get the response, use the update_evaluation tool to save the evaluation result into the database
5. Once get_next_skill_to_evaluate returns `None`, return a json with a single field `status` set to "done" to indicate completion
"""

EVALUATION_SYSTEM_PROMPT = """
{RECOMMENDED_PROMPT_PREFIX}

You are a specialised skill evaluator. Your job is to evaluate the candidate's proficiency in a given skill

1. Identify which skill you're evaluating (it will be mentioned in the conversation)
2. Use the get_question tool to get a question to ask (start with 'medium' difficulty). Ask the question verbatim, DO NOT MODIFY it in any way
3. After each candidate answer, use check_answer tool to evaluate
4. Decide the next question:
   - If the check_answer tool returned correct, choose the next higher difficulty, without going above 'hard'
   - If the check_answer tool returned incorrect, choose the lower difficulty, without going below 'easy'
   - Stop after 3 questions MAXIMUM
5. If the correctly answered two of the three questions, then they pass, otherwise they fail
6. After completion of 3 questions, hand off to the "Interview Orchestrator Agent" passing in the result of the evaluation

# DECISION RULES:

- Do not give feedback on the user's answer. Always proceed to the next question
- 3 questions per skill

# OUTPUT:

After the evaluation is complete, return the pass/fail in a json object with the following properties
- result: true or false
"""

ORCHESTRATOR_USER_PROMPT = """
Start an interview for the following values:

session_id: {session_id}
job_id: {job_id}

Begin by welcoming the applicant, extracting the key skills, then evaluate each one.
"""


def execute_triage_agent(session_id, job_id):
    triage_agent = Agent(
        name="Triage Agent",
        model="gpt-5.1",
        instructions=TRIAGE_PROMPT.format(
            RECOMMENDED_PROMPT_PREFIX=RECOMMENDED_PROMPT_PREFIX
        ),
        tools=[],
    )

    user_input = ORCHESTRATOR_USER_PROMPT.format(job_id=job_id, session_id=session_id)
    agent = orchestrator_agent
    while user_input != "bye":
        print(">>> Agent run:", agent.name)
        result = Runner.run_sync(agent, user_input, session=session, max_turns=20)
        agent = result.last_agent
        print(result.final_output)
        user_input = input("User: ")


def main():
    set_trace_processors(
        [
            BraintrustTracingProcessor(
                init_logger("Prodapt", api_key=settings.BRAINTRUST_API_KEY)
            )
        ]
    )
    job_id = 1
    session_id = "session123"
    run(session_id, job_id)
    print("FINAL EVALUATION STATE", db)


if __name__ == "__main__":
    main()
