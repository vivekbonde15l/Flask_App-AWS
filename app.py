import os
from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
import openai  # Import the openai library

# Initialize Flask app
app = Flask(__name__)

# Configure MySQL from environment variables
app.config['MYSQL_HOST'] = os.environ.get('MYSQL_HOST', 'localhost')
app.config['MYSQL_USER'] = os.environ.get('MYSQL_USER', 'default_user')
app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD', 'default_password')
app.config['MYSQL_DB'] = os.environ.get('MYSQL_DB', 'default_db')

# Initialize MySQL
mysql = MySQL(app)

# Initialize the OpenAI API with your API key
openai.api_key = os.environ.get('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')

@app.route('/')
def hello():
    cur = mysql.connection.cursor()
    cur.execute('SELECT message FROM messages')
    messages = cur.fetchall()
    cur.close()
    return render_template('index.html', messages=messages)

@app.route('/submit', methods=['POST'])
def submit():
    new_message = request.form.get('new_message')
    
    # Insert the user's message into the database
    cur = mysql.connection.cursor()
    cur.execute('INSERT INTO messages (message) VALUES (%s)', [new_message])
    mysql.connection.commit()
    cur.close()
    
    # Get an automatic reply using ChatGPT API
    reply = get_chatgpt_reply(new_message)
    
    # Insert the automatic reply into the database
    cur = mysql.connection.cursor()
    cur.execute('INSERT INTO messages (message) VALUES (%s)', [reply])
    mysql.connection.commit()
    cur.close()
    
    return redirect(url_for('hello'))

def get_chatgpt_reply(user_message):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"User: {user_message}\nAI:",
        max_tokens=50  # You can adjust the length of the reply
    )
    reply = response.choices[0].text.strip()
    return reply

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
