from flask import Flask
from app.routes import bp
 
app = Flask(__name__)
app.register_blueprint(bp)

def main():
    app.run(debug=True)

if __name__ == "__main__":
    main()