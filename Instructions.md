# Introduction
A number of sales meetings have been transcribed by an autonomous system and stored in files. These transcripts contain valuable insights that we wish to extract. Your task is to create a system that will automate extracting the required insights from the transcripts.


# The Data
The data is stored in individual text files in the transcripts directory. These are raw unprocessed transcripts.

Meetings typically involve 2 or more participants. Sometimes there is more than one person from the host company and sometimes more than one client present. Most transcripts take the form:

```
Host 1: That you used on your calls.

Client 2: Okay? But the underlying data is not available with fire. The underlying data cannot be this displayed for now. It's a right. So say you've used So icons it's. Over here and used help hubspot and five conversations. I mentioned thirty one times. Just click on this file. It should show me all the fine meetings that i've used this. You what right but don't stuff right. So currently, that's not available currently. Our team is working to towards it to get it. Enabled on the line.

Host 1: You said to get enabled... So, like, no matter what subscription I have. This is currently not.

Client 2: This is currently not available leave.

```

Where an individual speaker is identified as `Host x` or `Client x` depending on the role they play in the meeting.


# Requirements
Design and implement an API endpoint that, given a transcript, parses the transcript and extracts the following insights:

1. Did the client ask any questions? If they did identify the questions. For each question, determine if it is a meaningful question or not. 
  - For the purpose of this exercise, a meaningful question is not a greeting such as “How are you? Or other filler statements like “Can you hear me?”. 

2. List the next steps after the meeting is concluded. 

As a bonus you may wish to also find:
3. What is the overall tone of the client? Are they positive about the outcome of the meeting?
4. Did the client list any reasons why they will not buy the product? If so what was the reason?


# Deliverables
Write your code in the language and environment of your choice. A running version of your code should be accessible for demonstration purposes.

Provide:
A link to your code repository -- create a github repo (private or public depending on what Github's permissions are -- can private repos be "unlisted" or viewable via link?)
A link to your deployed API -- push up with ngrok (from ArchBox) | Deploy with some service like heroku
Any special instructions needed to execute your code -- Technical MD file (`readme` in the repo)


You should be prepared to discuss the following at your technical interview:
- A justification for the language, environment and third-party libraries that you used
- Details of your data processing steps (data cleaning, data exploration, problems with the data and so on)
- Details of your data analysis
- An explanation of your model and how your solution was implemented
- What difficulties did the data produce? What recommendation do you have for data gathering that will help improve the solution?




