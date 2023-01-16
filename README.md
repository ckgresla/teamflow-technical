# Teamflow Technical -- CKG




## Deployed API
I ended up deploying the system for question extraction + next step generation via a containerized flask app on a local desktop, making it public with `ngrok`, the deployed system should be live at- 
  * You can invoke the functions (addressed in questions 1 & 2 in the `Instruction.md` file) via POSTing to the Above URL at either;
    1. `/extract_questions`
    2. `/next_steps`
  * because of compute constraints and choice, I ended up using GPT-3 for most of the functionality, as a result the system is a bit slow and might take some time to parse through the transcript for the desired input--to--output.


## Sample Execution
In order to touch on the 3rd item in the deliverables list, I have included two files in the `sample_queries` dir -- here it shows how to make a request to the API with either cURL or in native python, building the docker container and deploying the API be accomplished if a user has access to a `OPENAI_TOKEN` and an ngrok account or linux-based machine with docker & public internet port access


## Data Gathering Suggestions
- Only include Client/Relevant calls: had a few transcripts where the only folks talking where in house names
  - transcripts like `63a074f3a39c8c8e9c0ebe2d.txt` are not really relevant to sales or meaningful client questions, why save them?
- Standardize Names: have a few calls with people like `betty white` or `ben ten` -- unless it makes sense to have specific names for some other function or reason we should anonymize these or treat them in the same manner as `client 1` or `host 1` entries
  - Also had one instance of a weird client name being saved- `'Client 2|Client 2'` in the `637cf23dcc7845331578f507.txt` file, the function for mapping speakers in transcripts should get looked at
