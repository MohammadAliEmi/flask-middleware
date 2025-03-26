from flask import request, jsonify
from collections import defaultdict
import time

class RateLimitMiddleware:
    def __init__(self, app, max_requests, window_seconds):
        self.app = app
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests = defaultdict(list)

    def __call__(self, environ, start_response):
        client_ip = environ.get('REMOTE_ADDR')
        current_time = time.time()

        # Remove outdated requests
        self.requests[client_ip] = [timestamp for timestamp in self.requests[client_ip] if current_time - timestamp < self.window_seconds]

        # Check if rate limit exceeded
        if len(self.requests[client_ip]) >= self.max_requests:
            res = jsonify({"error": "rate limit exceeded"})
            return res(environ, start_response)

        # Add current request timestamp
        self.requests[client_ip].append(current_time)

        return self.app(environ, start_response)

class DDoSProtectionMiddleware:
    def __init__(self, app, max_requests, window_seconds):
        self.app = app
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests = defaultdict(list)

    def __call__(self, environ, start_response):
        client_ip = environ.get('REMOTE_ADDR')
        current_time = time.time()

        # Remove outdated requests
        self.requests[client_ip] = [timestamp for timestamp in self.requests[client_ip] if current_time - timestamp < self.window_seconds]

        # Check if DDoS attack detected
        if len(self.requests[client_ip]) >= self.max_requests:
            res = jsonify({"error": "potential DDoS attack detected"})
            return res(environ, start_response)

        # Add current request timestamp
        self.requests[client_ip].append(current_time)

        return self.app(environ, start_response)
