import google.generativeai as genai
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
# Configure Gemini AI
genai.configure(api_key="AIzaSyB6FnJr5QNhtfE972ydklzCx_Rv9P4PChU")
model = genai.GenerativeModel("gemini-2.0-flash-exp")

# Flask App
app = Flask(__name__)
CORS(app, resources={r"/generate_code": {"origins": "*"}})  # Fix: Explicit CORS for endpoint

def generate_code(problem_details):
    title = problem_details.get('title', 'No Title')
    description = problem_details.get('description', 'No Description')
    format_details = problem_details.get('format', 'No I/O format provided')

    prompt = f"""// Disclaimer: Only output C code, nothing else.
    // Solve the following problem in C:
    //
    // Title: {title}
    //
    // Description:
    {description}
    //
    // Input/Output Format:
    {format_details}
    """

    response = model.generate_content(prompt).text
    res=response.split("```")[1][1:]
    return res

@app.route('/generate_code', methods=['POST'])
def generate_code_endpoint():
    problem_details = request.get_json()
    generated_code = generate_code(problem_details)
    return jsonify({'generatedCode': generated_code})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Railway assigns a dynamic port
    app.run(host="0.0.0.0", port=port)  # Ensure it binds to 0.0.0.0
