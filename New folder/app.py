from flask import Flask, render_template, request, jsonify
from Chatbot.langchain_service.langchain_service import generate_response


app = Flask(__name__)

@app.route("/")
def index():
    """
    Renders the main index page.

    :return: The rendered HTML template for the index page.
    """
    return render_template('index.html')


@app.route('/data', methods=['POST'])
def get_data():
    """
    Handles POST requests to process user data and generate a response.

    :return: A JSON response with the generated output.
        - response: Boolean indicating success.
        - message: The output generated from the user's input.
    :raises Exception: If the `generate_response` function encounters an error.
    """
    data = request.get_json()
    text=data.get('data')
    user_input = text
    # print(user_input)
    out = generate_response(user_input)
    print(out)
    return jsonify({"response":True,"message":out})

if __name__ == '__main__':
    app.run(debug=True)
