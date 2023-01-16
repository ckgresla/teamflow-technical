# If running these commands, make sure to run in `sample_queries` dir (the pointer to `transcript.json` assumes the terminal is currently @ this directory)
# If on Same Machine, can use localhost in URL, else use the provided url in the `README` for deployment version




# Question Extraction Sample --> returns extracted questions per client on the call
curl -H "Content-Type: application/json" -d @transcript.json localhost:5003/extract_questions

# Question Extraction Sample --> returns extracted questions per client on the call
curl -H "Content-Type: application/json" -d @transcript.json localhost:5003/next_steps


