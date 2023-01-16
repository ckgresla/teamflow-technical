# Wrapper for Question Extraction Code -- put on endpoint

import os

from flask import request, jsonify, make_response
# from download_hf_models import BrioSummarizer
from qe import *


class QuestionExtractionEndpoint():

    # Main Method
    def post(self):

        # Key for Text that needs to get summarized
        request_data = request.get_json()
        input_text = request_data.get("input_text") #expect just a regular string for the trancript -- will do other parsing here
        script_lines = transcript_lines(input_text)
        client_lines = parse_client_lines(script_lines)
        relevant_questions = parse_client_questions(client_lines)

        return make_response(jsonify(status="successful", relevant_questions=relevant_questions))

    # Request Handler -- moved in Logic for different request types from Main File
    def request_handler(self):
        if request.method == "POST":
            resp = self.post()
            return resp



