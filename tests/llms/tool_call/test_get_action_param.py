import pytest

from llms.tool_call import get_action_param


class Test_get_action_param:
    def test_multiple_actions_and_final_answer(self):
        text = """
Thought: The user has asked for two calculations. First, I need to calculate the area of a square with a side length of 5 cm. Then, I will calculate the area of a triangle with a base of 4 cm and a height of 6 cm. I'll start with the square's area.

Action: calculate_square_area_geometry_square_area__post
Action Input: {"side": 5}
Observation: {"area": 25}

Thought: Now that I have the area of the square, which is 25 square centimeters, I can proceed to calculate the area of the triangle as requested by the user.

Action: calculate_triangle_area_geometry_triangle_area__post
Action Input: {"base": 4, "height": 6}
Observation: {"area": 12}

Thought: I now know the final answer, having calculated both areas: the area of the square is 25 square centimeters, and the area of the triangle is 12 square centimeters.
Final Answer: The area of the square with a side length of 5 cm is 25 square centimeters, and the area of the triangle with a base of 4 cm and a height of 6 cm is 12 square centimeters.
"""
        res = get_action_param(text)
        expected = {
            "actions": [
                {"action_name": "calculate_square_area_geometry_square_area__post", "action_arguments": {"side": 5}},
                {"action_name": "calculate_triangle_area_geometry_triangle_area__post", "action_arguments": {"base": 4, "height": 6}},
            ],
            "final_answer": "The area of the square with a side length of 5 cm is 25 square centimeters, and the area of the triangle with a base of 4 cm and a height of 6 cm is 12 square centimeters.",
        }
        assert res == expected

    def test_single_action_and_final_answer(self):
        text = """
Thought: The user has asked for the area of a square with a side length of 5 cm.

Action: calculate_square_area_geometry_square_area__post
Action Input: {"side": 5}
Observation: {"area": 25}

Final Answer: The area of the square with a side length of 5 cm is 25 square centimeters.
"""
        res = get_action_param(text)
        expected = {
            "actions": [{"action_name": "calculate_square_area_geometry_square_area__post", "action_arguments": {"side": 5}}],
            "final_answer": "The area of the square with a side length of 5 cm is 25 square centimeters.",
        }
        assert res == expected

    def test_no_actions_only_final_answer(self):
        text = """
Thought: The user has asked for the final answer directly.

Final Answer: The final answer is provided without any calculations.
"""
        res = get_action_param(text)
        expected = {"actions": [], "final_answer": "The final answer is provided without any calculations."}
        assert res == expected

    def test_invalid_action_input(self):
        text = """
Thought: The user has asked for the area of a square, but provided invalid input.

Action: calculate_square_area_geometry_square_area__post
Action Input: {"side": "five"}
Observation: Invalid input.

Final Answer: The calculation could not be performed due to invalid input.
"""
        res = get_action_param(text)
        expected = {
            "actions": [{"action_name": "calculate_square_area_geometry_square_area__post", "action_arguments": {"side": "five"}}],
            "final_answer": "The calculation could not be performed due to invalid input.",
        }
        assert res == expected

    def test_no_final_answer(self):
        text = """
Thought: The user has asked for the area of a square with a side length of 5 cm.

Action: calculate_square_area_geometry_square_area__post
Action Input: {"side": 5}
Observation: {"area": 25}
"""
        res = get_action_param(text)
        expected = {"actions": [{"action_name": "calculate_square_area_geometry_square_area__post", "action_arguments": {"side": 5}}], "final_answer": ""}
        assert res == expected
