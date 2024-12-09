import json
import traceback

from llm.prompt import PROMPT_REACT, PROMPT_TOOL, TOOL_DESC
from util.request import get_json, post_json


def get_messages4tool(messages, tools):
    prompt = generate_action_prompt(messages, tools)
    print("prompt:", prompt)
    messages4tool = [{"role": "user", "content": prompt}]
    return messages4tool


def get_messages4answer(messages, tool_result):
    messages4answer = messages + [
        {
            "role": "assistant",
            "content": PROMPT_TOOL.format(tool_result=json.dumps(tool_result)),
        },
    ]
    return messages4answer


def get_tool_from_api(openapi_json):
    tool_arr = []
    for path_key, path_val in openapi_json["paths"].items():
        for method_key, method_val in path_val.items():
            if "tool" not in method_val.get("tags", []):
                continue
            tool = {"name_for_model": method_val["operationId"], "name_for_human": "%s %s" % (method_key, path_key), "description_for_model": method_val["summary"]}
            tool["parameters"] = method_val.get("parameters", [])
            tool["path_key"] = path_key
            tool["method_key"] = method_key
            tool["method_val"] = method_val
            tool_arr.append(tool)
    return tool_arr


def generate_action_prompt(query, tools):
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

    action_prompt = PROMPT_REACT.format(tool_descs=tool_descs_str, tool_names=tool_names_str, query=query)
    return action_prompt


def get_action_param(text: str):
    action_index = text.rfind("\nAction:")
    action_input_index = text.rfind("\nAction Input:")
    observation_index = text.rfind("\nObservation:")

    if 0 <= action_index < action_input_index:
        if observation_index < action_input_index:
            text = text.rstrip() + "\nObservation:"
            observation_index = text.rfind("\nObservation:")

    if 0 <= action_index < action_input_index < observation_index:
        action_name = text[action_index + len("\nAction:") : action_input_index].strip()
        action_arguments = text[action_input_index + len("\nAction Input:") : observation_index].strip()
        res = {"action_name": action_name, "action_arguments": action_arguments}
        return res

    final_answer_index = text.rfind("\nFinal Answer:")
    res = {"final_answer": text[final_answer_index + len("\nFinal Answer:") :].strip()}
    return res


async def execute_tool(response, tools, base_url):
    plugin_configuration = get_action_param(response)
    result_dict = {"status_code": 200}
    final_answer = plugin_configuration.get("final_answer")
    if final_answer:
        result_dict["result"] = final_answer
        return result_dict
    first_config_line = plugin_configuration["action_arguments"].split("\n")[0]
    config_parameters = json.loads(first_config_line)
    for tool in tools:
        if tool["name_for_model"] != plugin_configuration["action_name"]:
            continue
        url = f"{base_url}{tool['path_key']}"
        try:
            if tool["method_key"] == "get":
                result_dict["url"] = url
                result_dict["result"] = await get_json(url, {})
            elif tool["method_key"] == "post":
                param_path = "&".join([f"{key}={val}" for key, val in config_parameters.items()])
                if param_path:
                    url += "?%s" % param_path
                result_dict["url"] = url
                result_dict["result"] = await post_json(url, {})
            else:
                result_dict["result"] = "Unknown method"
        except Exception as ex:
            result_dict["status_code"] = 500
            result_dict["msg"] = str(ex)
            result_dict["detail"] = traceback.print_exc()
        return result_dict

    result_dict["status_code"] = 404
    result_dict["msg"] = "No matching tool found"
    return result_dict
