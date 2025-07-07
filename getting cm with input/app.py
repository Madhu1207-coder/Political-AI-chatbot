from flask import Flask, render_template, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

# Configure the API
api_key = "YOUR_API_KEY"  # Add your actual API key here
genai.configure(api_key=api_key)

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-2.0-flash-exp",  # This should be the correct model name
    generation_config=generation_config,
    system_instruction="Political details about India",
)

# Initialize chat session
chat_session = model.start_chat(history=[])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    try:
        # Extract the user's question from the form data
        user_question = request.form['question']
        
        # Send the message to the chat session
        response = chat_session.send_message(user_question)
        
        # Return the response as a JSON object
        return jsonify({'response': response.text})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
