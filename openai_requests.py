import os
import requests
import numpy as np
import warnings

warnings.filterwarnings("ignore")




# Configure Tokens + OpenAI's API Endpoints
openai_auth_token = os.getenv("CKG_OPENAI_API_TOKEN") 
OPENAI_API_URL = "https://api.openai.com/v1/completions"
OPENAI_EMBEDDINGS_URL = "https://api.openai.com/v1/embeddings"


question_parse_prompt = """
Your job is to parse transcripts of client calls at a software company in order to extract relevant questions for us to address with our clients, given a sequence of "Input_Text" please identify any questions, relevant to software or the company, by repeating them on new lines. If the client does not ask any questions that are relevant to software or technology; please write `NO_QUESTIONS` to help us understand the transcripts.

###
Input_Text: 
Right? So I I still don't think we'd be ready you know, February... Our fiscal years February to January. I don't think we'd be ready February one for implementation anyway. I do got... We've got a lot of clean we have to do on our end both from a Salesforce ai perspective, and the upgrades is working on and get that. Data in the Salesforce and get a clean, and also from a next perspective we've got a ton of stuff is not in the right, You know, there need to be rec class. The things are that lot of turnover accounting and things aren't coded to the right department. So you know, it'd be the the classic of garbage garbage out. If we actually, you know, it went today so definitely why I take the time to do the data cleanup knob and and whatnot. Yeah. Like, like I said, the the vendors that we looked at last year are kinda, hey, what do you think? And, you know, one of them offered us, you know, a very good deal and we could push the implementation after for three months. Right? So I kinda wanna I wasn't planning on looking at this this quickly. But if... you know, and then our Cfo in some Cfo group. And someone said mosaic jose was a good tool so he wants us to to at least look at mosaic before we make that type of decision.

Mosaic Jose is a good tool? Do you offer support for that? 
Do you think you'd be ready for implementation by February 1st? 
What type of data clean up needs to be done? 
What vendors did you look at last year?
###
Input_Text: 
"""
    #just insert the text we want classified to the end of prompt


# Get Embeddings from OpenAI
def get_embedding(text, model="text-search-ada-doc-001"):
    # Given a string of text, return embeddings from OpenAI (presumably each sentence in original text gets passed as an embedding)
    #list of Embedding Models- https://beta.openai.com/docs/guides/embeddings/types-of-embedding-models (Text Search Models might be the choice for this task)

    # text = text.replace("\n", " ") #recommended for higher quality embeddings via the OpenAI team, may or may not be useful if we already pass in sentences
    # OpenAI API Call (not brain auth)
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai_auth_token}" #brain has diff authorization scheme
    }
    payload = {
        "model": f"{model}",
        "input": f"{text}"
    }
    response = requests.post(OPENAI_EMBEDDINGS_URL, json=payload, headers=headers, verify=False) #avoid SSL Certificate Issue by passing "verify=False"
    response_data = response.json() #get JSON back from response object
    # print(response_data)
    embedding = response_data['data'][0]['embedding'] #parse JSON for embeddings info

    # embedding = openai.Embedding.create(input=[text], model=model)['data'][0]['embedding'] #returns a list of the embedding values (if importing openai, switched to manual method above, issue with OpenAI Lib (dependency conflict w Brain Container)
    embedding = np.array(embedding) #convert to array for better speed & space
    return embedding


# Generation Function (for a given prompt file)
def get_completion(input_text: str, prompt=None, max_tokens=1000, model="text-davinci-003", n=1, stream=False, stop=None, temperature=0.8, top_p=1, frequency_penalty=0, presence_penalty=0):
    """
    Same Defaults in func call as per OpenAI Docs
    see- https://beta.openai.com/docs/api-reference/completions/create
    """

    if os.path.exists(prompt):
        with open(prompt, "r") as f:
            prompt = f.read().replace('\\n', '\n').strip() #JSON compatible
            f.close()
    else:
        prompt = prompt

    completition_prompt = prompt + input_text #method of adding text to prompt (assumes that input_text var will contain the text formatted like the prompt for the model's generation)

    # Make Request, see- https://beta.openai.com/docs/api-reference/models/list
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai_auth_token}" #brain has diff authorization scheme (diff keyword than "Bearer")
    }
    payload = {
        "model": f"{model}",
        "max_tokens": max_tokens, #default we can change
        "n" : n,                  #num generations
        "stream" : stream,
        "stop" : stop,
        "prompt": completition_prompt,
        "presence_penalty": presence_penalty,
        "frequency_penalty": frequency_penalty,
        "top_p" : top_p,
        "temperature" : temperature #see- https://beta.openai.com/docs/api-reference/completions/create#completions/create-temperature
    }

    # Assumes Generation will not be longer than max sequence len
    response = requests.post(OPENAI_API_URL, json=payload, headers=headers, verify=False)
    response_data = response.json() #get JSON back from response object
    generation = response_data["choices"][0]['text'].strip()

    return generation



if __name__ == "__main__":
    sample_prompt = """
Your job is to parse transcripts of client calls at a software company in order to extract relevant questions for us to address with our clients, given a sequence of "Input_Text" please identify any questions, relevant to software or the company, by repeating them on new lines. If the client does not ask any questions that are relevant to software or technology; please write `NO_QUESTIONS` to help us understand the transcripts.

###
Input_Text: 
Right? So I I still don't think we'd be ready you know, February... Our fiscal years February to January. I don't think we'd be ready February one for implementation anyway. I do got... We've got a lot of clean we have to do on our end both from a Salesforce ai perspective, and the upgrades is working on and get that. Data in the Salesforce and get a clean, and also from a next perspective we've got a ton of stuff is not in the right, You know, there need to be rec class. The things are that lot of turnover accounting and things aren't coded to the right department. So you know, it'd be the the classic of garbage garbage out. If we actually, you know, it went today so definitely why I take the time to do the data cleanup knob and and whatnot. Yeah. Like, like I said, the the vendors that we looked at last year are kinda, hey, what do you think? And, you know, one of them offered us, you know, a very good deal and we could push the implementation after for three months. Right? So I kinda wanna I wasn't planning on looking at this this quickly. But if... you know, and then our Cfo in some Cfo group. And someone said mosaic jose was a good tool so he wants us to to at least look at mosaic before we make that type of decision.

Mosaic Jose is a good tool? Do you offer support for that? 
Do you think you'd be ready for implementation by February 1st? 
What type of data clean up needs to be done? 
What vendors did you look at last year?
###


    """

    txt = """
    Input_Text: 
 "Client 4: required to put in So know, one of things like I said, we have and they have like what do we churn the customer. Right? We have a renewal is open, but if it doesn't close at the certain time we combat that churn. There's some ambiguity with regard to you know, when account that is churn. And then the other question, they'll probably have is on our revenue the process was such that either the person is not only here, we're just kinda grouping all of our revenue for a customer in online. And sending invoice where the customer may have a platform subscription an it's response retainer so else, all that was being bucket on online, so really can it's impossible for us to look at like, pull salesforce report four eight given customer product and see if there we're still a recognizing revenue on we don't track things at that level.",
    """
    out = get_completion(txt, sample_prompt)
    print(out)