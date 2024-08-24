"""
This module handles the loading of test data, word data, 
and questions for the English learning Telegram bot.

It imports utility functions from `json_utils` and `questions_loader` to load the necessary data
for quizzes and word tests.
"""

from .json_utils import (
    load_test_data,
    load_words_data
)
from .questions_loader import load_questions
