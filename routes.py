import json
import logging
import account_client

from flask import Flask, request

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)


@app.route('/connect', methods=['GET'])
def connect_with_social_platform():
    return json.dumps(account_client.create_or_update_existing_profile(request.args.get('token')))

if __name__ == "__main__":
    app.run()