import json
import re
import traceback
from typing import Dict, List

import aiohttp
from termcolor import colored

from llms.prompt import TOOL_DESC


def get_messages4tool(messages, tools, prompt):
    prompt = generate_action_prompt(messages, tools, prompt)
    print(colored(prompt, "green"))
    messages4tool = [{"role": "user", "content": prompt}]
    return messages4tool


def get_messages4answer(messages, tool_result, prompt):
    prompt = prompt.format(tool_result=json.dumps(tool_result))
    print(colored(prompt, "green"))
    messages4answer = messages + [
        {
            "role": "assistant",
            "content": prompt,
        },
    ]
    return messages4answer


def get_tool_from_api(openapi_json):
    tools = []
    for path_key, path_val in openapi_json["paths"].items():
        for method_key, method_val in path_val.items():
            if "tool" not in method_val.get("tags", []):
                continue
            tool = {"name_for_model": method_val["operationId"], "name_for_human": "%s %s" % (method_key, path_key), "description_for_model": method_val["summary"]}
            tool["parameters"] = method_val.get("parameters", [])
            tool["path_key"] = path_key
            tool["method_key"] = method_key
            tool["method_val"] = method_val
            tools.append(tool)
    return tools


def generate_action_prompt(messages, tools, prompt):
    tool_descs = []
    tool_names = []

    for info in tools:
        tool_descs.append(
            TOOL_DESC.format(
                name_for_model=info["name_for_model"],
                name_for_human=info["name_for_human"],
                description_for_model=info["description_for_model"],
                parameters=json.dumps(info["parameters"], ensure_ascii=False),
            )
        )
        tool_names.append(info["name_for_model"])

    tool_descs_str = "\n\n".join(tool_descs)
    tool_names_str = ",".join(tool_names)
    history = []
    if len(messages) > 1:
        history = messages[:-1]
    messages = messages[-1:]
    action_prompt = prompt.format(tool_descs=tool_descs_str, tool_names=tool_names_str, query=messages, history=history)
    return action_prompt


def is_finished(tool_response: str) -> bool:
    completion_keywords = ["Task complete", "Finished", "All done"]
    for keyword in completion_keywords:
        if keyword in tool_response:
            return True
    return False


def extract_actions(text):
    actions_pattern = r"Action:\s*(.*?)\nAction Input:\s*(.*?)\n"
    actions = re.findall(actions_pattern, text, re.DOTALL)
    actions_list = []
    for action_name, action_input in actions:
        try:
            action_arguments = json.loads(action_input)
            actions_list.append({"action_name": action_name.strip(), "action_arguments": action_arguments})
        except json.JSONDecodeError:
            continue
    return actions_list


def extract_final_answer(text):
    final_answer_match = re.search(r"Final Answer:\s*(.*)", text, re.DOTALL)
    if final_answer_match:
        return final_answer_match.group(1).strip()
    return ""


def extract_finished(text):
    final_answer_match = re.search(r"Finished:\s*(.*)\n", text, re.DOTALL)
    if final_answer_match:
        return final_answer_match.group(1).strip()
    return ""


def get_action_param(text: str):
    actions = extract_actions(text)
    final_answer = extract_final_answer(text)
    finished = extract_finished(text)
    return {"actions": actions, "final_answer": final_answer, "finished": finished}


async def execute_tool(response: str, tools: List[Dict], base_url: str) -> Dict:
    plugin_config = get_action_param(response)
    plugin_config["status_code"] = 200
    tool_map = {tool["name_for_model"]: tool for tool in tools}
    tool_results = []
    for action in plugin_config.get("actions", []):
        action_name = action.get("action_name")
        action_arguments = action.get("action_arguments", {})
        tool = tool_map.get(action_name)
        if tool:
            result = await execute_tool_request(tool, base_url, action_arguments)
            tool_results.append(result)
    if tool_results:
        plugin_config["tool_results"] = tool_results
        return plugin_config
    final_answer = plugin_config.get("final_answer")
    if final_answer:
        return plugin_config
    return {"status_code": 500, "msg": "No final_answer tool found"}


async def execute_tool_request(tool: Dict, base_url: str, action_arguments: Dict) -> Dict:
    url = base_url + tool["path_key"]
    method = tool["method_key"].lower()
    try:
        if method == "get":
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    response_data = await response.json()
        elif method == "post":
            async with aiohttp.ClientSession() as session:
                async with session.post(url, params=action_arguments) as response:
                    response_data = await response.json()
        else:
            return {"status_code": 500, "msg": "Unknown method"}
        return {"status_code": 200, "result": response_data, "url": url}
    except Exception as ex:
        return {"status_code": 500, "msg": str(ex), "detail": traceback.format_exc()}
