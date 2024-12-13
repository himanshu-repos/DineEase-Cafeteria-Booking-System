from flask import Flask, render_template
import subprocess

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/start_user_gui')
def start_user_gui():
    # Run the user_gui.py script
    subprocess.Popen(['python', 'user_gui.py'])
    return "User GUI is starting..."

if __name__ == '__main__':
    app.run(debug=True)
