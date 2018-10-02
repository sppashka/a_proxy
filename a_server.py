# coding : utf-8
"""
Simple server that reverse world and will use JSON
"""

import json
from flask import Flask, request, make_response as response

APP = Flask(__name__)


@APP.route("/")
def index():
    """Generator one page"""
    text = request.args.get('text')
    json_type = 'application/json'
    json_accepted = json_type in request.headers.get('Accept', '')
    if text:
        words = text.split()
        reversed_words = [word[::-1] for word in words]
        if json_accepted:
            res = response(json.dumps({'text': reversed_words}), 200)
        else:
            res = response(' '.join(reversed_words), 200)
    else:
        res = response('text not found', 501)
    res.headers['Content-Type'] = json_type if json_accepted else 'text/plain'
    return res

if __name__ == "__main__":
    APP.run(host='0.0.0.0', port=8081)
