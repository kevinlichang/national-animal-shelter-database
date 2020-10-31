from flask import Flask, render_template, url_for

app = Flask(__name__)

@app.route("/")
def main():
    return "Hello"

if __name__ == '__main__':
    app.run(debug=True)