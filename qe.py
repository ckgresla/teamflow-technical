# Utils to Power the Question Endpoint

import os




# Get Statistics from a Transcript (n people + n lines per person for a single file/transcript str)
def transcript_stats(script: str=None):
    """
    Function to get a list of lines spoken and speaker stats for a given;
      - Transcript String
      - Transcript Filepath
    """
    # Case When script is path on disk
    if os.path.exists(script):
        file = open(script)
        data = file.read()
        data = data.split("\n")
    # Else if not a path, assume passed string *is* the script
    else:
        data = script
    
    # Remove LITERAL duplicate strs + get number of speakers and info
    data = data.split("\n")
    data = set(data)
    if "" in data:
        data.remove("") #remove the empty line chars
    stats = {}

    for seq in data:
        speaker = seq.split(":")[0] #assuming that real data follows sample conventions
        if speaker not in stats:
            stats[speaker] = 0
        else: 
            stats[speaker] += 1

    stats["n_people"] = len(stats) #number of folks in transcription str
    return data, stats


