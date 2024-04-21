from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import requests

app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# Load the OpenAI API key from the environment variable
api_key = os.getenv('OPENAI_API_KEY')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        # Get the message from the request JSON
        message = request.json['message']
        print(message)

        # Define the OpenAI API URL
        url = "https://api.openai.com/v1/chat/completions"

        # Set up the headers with the API key and the model you want to use
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }

        # Prepare the data payload
        payload = {
            "model": 'gpt-3.5-turbo',
            #"prompt": f"{message}\nAI:",
            "messages": [
                {"role": "user", "content": message}
            ],
            #"max_tokens": 150,
            "temperature": 0.5  # Adjust temperature for generating diverse responses
        }

        # Make the POST request to the OpenAI API
        response = requests.post(url, headers=headers, json=payload)
        print(response.json()['choices'][0]['message']['content'])

        try:
            return response.json()['choices'][0]['message']['content']
        except KeyError:
            return "Error or no response"
        
        # Check for errors
        '''if response.status_code == 200:
            # Extract the response from the API
            
            return response.json
        else:
            # If there's an error, return an error message
            return jsonify({"response": "Failed to call OpenAI API."}), 500'''

    except Exception as e:
        # Print the exception error message to the console
        print(f"An error occurred: {str(e)}")
        # Return an error response
        return jsonify({"response": "An error occurred."}), 500

if __name__ == '__main__':
    app.run(debug=True)


'''
def chat():
    try:
        message = request.json['message']
        #print(message)
        response = client.completions.create(model='gpt-3.5-turbo',
        prompt=f"User: {message}\nAI:",
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.7)
        if response.choices[0].text.strip():
            return jsonify({"response": response.choices[0].text.strip()})
        else:
            return jsonify({"response": "Sorry, I don't have a response for that."})
    except Exception as e:
        print(f"Exception: {str(e)}")
        return jsonify({"response": "Sorry, something went wrong."})
'''

