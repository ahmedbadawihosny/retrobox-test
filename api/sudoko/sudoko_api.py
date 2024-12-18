from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/sudoko')
def home():
    return 'Hello, Sudoko!'

if __name__ == '__main__':
    app.run(debug=True)
