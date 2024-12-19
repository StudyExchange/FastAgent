TOOL_DESC = """{name_for_model}: Call this tool to interact with the {name_for_human} API. What is the {name_for_human} API useful for: {description_for_model} Parameters:{parameters}
"""

PROMPT_REACT = """
First, think about how to respond to the user's message. 
Then, if there is an available tool to call, do not answer the questions directly. Or not, answer the following questions as best you can. 
You have access to the following:
{tool_descs}

Use the following format:
History: a list of past interactions (if any)
Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can be repeated zero or more times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!
History: {history}
Question: {query}
"""

PROMPT_ANSWER = """
Answer the user's question based on the tool call result.
The result of the tool call is as follows:
{tool_result}
"""