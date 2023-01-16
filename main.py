# Flask API
from flask import Flask, jsonify, request


# Instantiate App
app = Flask(__name__)

# Port to Serve API
PORT_TO_SERVE = 5003


# Define Routes per Model Endpoint/Controller
# Model responses are JSON-ified in the respective controller files

# Health Handler
@app.route("/health", methods=['GET','POST'])
def health():
    if request.method=='GET':
        return dict(greeting="This is my Teamflow Technical Endpoint, Welcome!"), 200
    else:
        return jsonify({'Error':"Sorry, the '/health' endpoint accepts GETs"})

# Next Steps Endpoint -- given transcript, generate the next steps bullet point list
from controllers.summarizers import NextStepsEndpoint
NS = NextStepsEndpoint()
app.add_url_rule("/next_steps", "next_steps", NS.request_handler, methods=["GET", "POST"])

# Question Extraction Endpoint -- given transcript, parse our relevant client questions
from controllers.question_extraction import QuestionExtractionEndpoint
QE = QuestionExtractionEndpoint()
app.add_url_rule("/extract_questions", "extract_questions", QE.request_handler, methods=["POST"])


# Run App on Configured Port
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=PORT_TO_SERVE) #port specified in settings


