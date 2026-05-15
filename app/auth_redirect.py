from urllib.parse import urlencode
from flask_cors import CORS
import requests
from flask import (
    Blueprint,
    Response,
    jsonify,
    request,
    redirect,
)

from app import CONFIGURATION

authorization_endpoint = Blueprint("authorization_endpoint", __name__, url_prefix="/")
CORS(authorization_endpoint)


@authorization_endpoint.route("/pushed_authorization", methods=["POST"])
def pushed_authorization():

    print("\nrequest body: ", request.form.to_dict(), flush=True)
    print("\nrequest headers: ", request.headers, flush=True)

    try:
        if request.content_type and "application/json" in request.content_type:
            body = request.get_json()
        else:
            # Convert form data to dict
            body = request.form.to_dict()

        body["frontend_id"] = CONFIGURATION["frontend_id"]

        forward_headers = {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Accept": "application/json,application/json",
            "Accept-Charset": "UTF-8",
            "User-Agent": request.headers.get("User-Agent", "proxy-service"),
        }

        response = requests.post(
            f"{CONFIGURATION['oauth_url']}/pushed_authorization",
            data=body,  # Send as form data
            headers=forward_headers,
            timeout=30,
        )

        return response.content, response.status_code, response.headers.items()

    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Proxy request failed", "details": str(e)}), 502
    except Exception as e:
        return jsonify({"error": "Internal server error", "details": str(e)}), 500
