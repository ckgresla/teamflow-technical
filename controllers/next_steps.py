# Controller for Summarization & Next Steps Generation
import os
import time

from flask import request, jsonify, make_response
from download_hf_models import BrioSummarizer




# Need Instantiate a Model Object (to access the attributes)
brio = BrioSummarizer()


class NextStepsEndpoint():

    # Generate Summaries for given inputs
    def generate_summary(self, input_text: list)-> list:
        summary_text = brio.summarize(input_text) #expects a string, not list of strings
        return brio.bpf(summary_text) #returns bpf'd output, can swap for below -- a list of results
        # return summary_text #returns paragraph-esque summary


    # Main Method -- expects a transcript string as in request_data
    def post(self):

        # Key for Text that needs to get summarized
        # request_data = request.get_json() #expect following vars in the request
        # input_text = request_data.get("input_text")
        input_text = sample_txt #TODO: comment out the above and delete this -- used for testing the endpoint locally
        input_tokens = brio.tokenizer.tokenize(input_text) #get tokens for input

        # Check Length, Trim if longer than max context for Model
        print("Lengths of Input & Model Limit", len(input_tokens), brio.max_length)
        if len(input_tokens) >= brio.max_length:
            print("Webpage Content too long for Model, trimming into Sequences")
            # input_text = (input_tokens[i:i + brio.max_length] for i in range(0, len(input_tokens), brio.max_length))
            input_text = list((input_tokens[i:i + brio.max_length] for i in range(0, len(input_tokens), brio.max_length)))
        else:
            input_text = [input_tokens] #whole transcript fits in context

        summarized_text = [] #to hold the summary strings
        sequence_count = 0 #count of sequences to summarize
        total_time = elapsed_time = time.monotonic()
        print(f"\nGenerating Summaries for {len(input_text)} Sequences")

        for sequence in input_text:
            start_time = time.monotonic()
            sequence_summaries = self.generate_summary(sequence) #generate summary of content per max token len sequence

            for summary in sequence_summaries:
                summarized_text.append(summary) #list of strings per bullet point
            end_time = time.monotonic()
            time_diff = end_time - start_time
            elapsed_time += time_diff #to track total time for all summaries
            sequence_count += 1
            print(f"  Sequence {sequence_count} summarized in {time_diff:.2f}s")
        print(f"Completed Summarization of Doc in: {elapsed_time - total_time:.2f}s")


        # Return Summarized String, if not empty list
        if summarized_text != []:
            summarized_text = "\n".join(summarized_text)
            summarized_text = summarized_text.replace(" ", "")
            # print(type(summarized_text)) #debugging
            print(summarized_text) #view output, serverside
            return make_response(summarized_text, 200)
        else:
            return make_response("Summary Generation Error", 400)


    # Get Request Handler, mainly to check server's home dir & health of endpoint
    def get(self):
        print("Get Request Successful to Summarize Endpoint Successful")
        #output = f"Path: {os.curdir} & Contents{os.listdir()}"
        output = "Summary Endpoint- requires text to be passed via a JSON 'input_text' key\n"
        return make_response(output)


    # Request Handler -- moved in Logic for different request types from Main File
    def request_handler(self):
        if request.method == "GET":
            resp = self.get()
            return resp
        elif request.method == "POST":
            resp = self.post()
            return resp


