from flask import Flask, render_template, request, jsonify
from Chatbot.langchain_service.langchain_service import generate_response

user_message = 'Write a paragraph about life on Mars in year 2100.'
response = generate_response(user_message)
print(response.content)

