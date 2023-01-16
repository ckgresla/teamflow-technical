# CKG Module for HF Model Spin Up

import os
import pickle #for saving binarized models
import torch
import transformers #for checking the version being used
from transformers import BartTokenizer, BartForConditionalGeneration, PegasusTokenizer, PegasusForConditionalGeneration #summarizing module
from transformers import AutoTokenizer, AutoModel

from transformers import logging




# Make dir for Models if not exist
if not os.path.exists("models"):
    os.makedirs("models")

print("Transformer Version: ", transformers.__version__)
print("Torch Version: ", torch.__version__)

print("Models Dir:", os.listdir("models"))


# Utility Code
def model_artifacts_download(model):
    # Tokenizer
    with open(f"./models/{model.name}-Tokenizer.pt", 'wb') as fh:
        pickle.dump(model.tokenizer, fh)

   # Model Weights
    with open(f"./models/{model.name}-Model.pt", 'wb') as fh:
        pickle.dump(model.model, fh)
    return




# Generate Summaries with BRIO
class BrioSummarizer():
    def __init__(self):
        super().__init__()
        # Instantiate Summarizer Model
        self.IS_CNNDM = True #false uses XSUM dataset & Pegasus Model (Pegasus trained for GAP Sentence Pred as opposed to CNN-DM BRIO)
                        #anecdotally, XSUM returns shorter summaries and CNN-DM returns multi points
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.max_length = 1024 if self.IS_CNNDM else 512 #CNN/DM dataset has longer summarization len
        self.max_length = 512 #run out of memory if trying to compute w true max len
        self.model_name = 'Yale-LILY/brio-cnndm-uncased'
        self.name = "BRIO-cnndm-uncased"

        logging.set_verbosity_warning() #remove annoying warning, not training here
        logging.set_verbosity_error() #remove really annoying warning

        # Load in Pre-Trained Model (can save models to disk as if it speeds up load-in/inference)
        if self.IS_CNNDM:
            # BART Pre-Trained
            artifact_path = os.path.join("models", f"{self.name}-Tokenizer.pt")
            if os.path.isfile(artifact_path):
                print(f"Loading in Tokenizer for {self.name} from Disk")
                file_to_unpickle = open(artifact_path, "rb")
                self.tokenizer = pickle.load(file_to_unpickle)
            else:
                print(f"Loading in Tokenizer for {self.name} from HF")
                self.tokenizer = BartTokenizer.from_pretrained('Yale-LILY/brio-cnndm-uncased')

            artifact_path = os.path.join("models", f"{self.name}-Model.pt")
            if os.path.isfile(artifact_path):
                print(f"Loading in Model- {self.name} from Disk")
                file_to_unpickle = open(artifact_path, "rb")
                self.model = pickle.load(file_to_unpickle)
                print("") #newline after completing model load
            else:
                print(f"Loading in Model- {self.name} from HF")
                self.model = BartForConditionalGeneration.from_pretrained('Yale-LILY/brio-cnndm-uncased')
                print("") #newline after completing model load
        else:
            # Pegasus Pre-Trained
            artifact_path = os.path.join("models", f"{self.name}-Tokenizer.pt")
            if os.path.isfile(artifact_path):
                print(f"Loading in Tokenizer for {self.name} from Disk")
                file_to_unpickle = open(artifact_path, "rb")
                self.tokenizer = pickle.load(file_to_unpickle)
            else:
                print("Loading in Tokenizer from HF")
                self.tokenizer = PegasusTokenizer.from_pretrained('Yale-LILY/brio-xsum-cased')

            artifact_path = os.path.join("models", f"{self.name}-Model.pt")
            if os.path.isfile(artifact_path):
                print(f"Loading in Model- {self.name} from Disk")
                file_to_unpickle = open(artifact_path, "rb")
                self.model = pickle.load(file_to_unpickle)
                print("") #newline after completing model load
            else:
                print(f"Loading in Model- {self.name} from HF")
                self.model = PegasusForConditionalGeneration.from_pretrained('Yale-LILY/brio-xsum-cased')
                print("") #newline after completing model load

    # Split Sequences into Summarizable Chunks
    def sequence_splitter(self, transcript: str):
        result = self.tokenizer.tokenize(transcript)

        return result

    # Generate Summary
    def summarize(self, article):
        print("article len: ", len(article))
        print(article, "\n\n\n\n\n\n\n\n\n\n\n")
        inputs = self.tokenizer(article, max_length=self.max_length, return_tensors="pt", padding=True, truncation=True)
        inputs.to(self.device) #gofast
        self.model.to(self.device) #gofast
        summary_ids = self.model.generate(inputs["input_ids"])
        output = self.tokenizer.batch_decode(summary_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0]
        return output #can format by calling bpf func on this

    # Format Summary Output -- convert sentences into Bullet Points
    def bpf(self, txt):
        bps = []
        for t in txt.split(". "):
            # t = t.strip(".").title() #nice casing for Bullet Points
            t = t.strip(".") #regular sentence casing
            bp = f"- {t}"
            # print(bp)
            bps.append(bp)
        return bps


# Download Model Artifacts if Script is run
if __name__ == "__main__":

    # Summarization Model
    BRIO = BrioSummarizer()
    model_artifacts_download(BRIO)
    txt = "TESTING !@#" * 320

    out = BRIO.sequence_splitter(txt)
    print(len(out))

