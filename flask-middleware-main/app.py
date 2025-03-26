from flask import Flask, jsonify
from middleware import RateLimitMiddleware, DDoSProtectionMiddleware

app = Flask(__name__)

app.wsgi_app = RateLimitMiddleware(app.wsgi_app, max_requests=100, window_seconds=60)
app.wsgi_app = DDoSProtectionMiddleware(app.wsgi_app, max_requests=200, window_seconds=60)

@app.route('/')
def home():
    return jsonify({"message": "Hello, World!"})

if __name__ == '__main__':
    app.run()
