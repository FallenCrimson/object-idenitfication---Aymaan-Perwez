from flask import Flask, render_template, request, jsonify
import subprocess

app = Flask(__name__)

def execute_option(option):
    if option == 1:
        subprocess.run(['python', 'amo.py'])
    elif option == 2:
        subprocess.run(['python', 'second.py'])
    elif option == 3:
        subprocess.run(['python', 'regards.py'])
    elif option == 0:
        return "Exiting program."
    else:
        return "Invalid option"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/run_program', methods=['POST'])
def run_program():
    data = request.get_json()
    user_choice = int(data.get('user_choice', 0))  # Convert user_choice to an integer

    if not 0 <= user_choice <= 3:
        return jsonify({"error": "Invalid option"}), 400

    result = execute_option(user_choice)
    
    if result == "Exiting program.":
        return jsonify({"result": result})
    else:
        return jsonify({"result": "Program executed."})

if __name__ == "__main__":
    app.run(debug=False, port=5001)  # Change the port number (e.g., 5001)
