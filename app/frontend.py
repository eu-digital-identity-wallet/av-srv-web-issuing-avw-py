import base64
import io
import json
import urllib
from urllib.parse import quote, urlencode
from flask_cors import CORS
import requests
import logging
from flask import (
    Blueprint,
    Response,
    make_response,
    request,
    redirect,
    render_template,
    url_for,
    jsonify,
)

from app import oidc_metadata, openid_metadata, signed_metadata
from app import CONFIGURATION

frontend = Blueprint("frontend", __name__, url_prefix="/")
CORS(frontend)

logger = logging.getLogger(__name__)


@frontend.route("/display_auth_method", methods=["POST"])
def display_auth_method():
    raw_json_string = request.form.get("payload")

    logger.info(f"raw_json_string: {raw_json_string}")

    if raw_json_string:
        try:

            data_payload = json.loads(raw_json_string)
            logger.info(f"data_payload: {data_payload}")

        except json.JSONDecodeError:
            return jsonify({"status": "error", "message": "Invalid JSON payload"}), 400

        session_id = data_payload.get("session_id")
        logger.info(f"session_id: {session_id}")
        pid_auth = data_payload.get("pid_auth")
        logger.info(f"pid_auth: {pid_auth}")

        country_selection = data_payload.get("country_selection")
        logger.info(f"country_selection: {country_selection}")

        redirect_url = data_payload.get("redirect_url")
        logger.info(f"redirect_url: {redirect_url}")

        return render_template(
            "misc/auth_method.html",
            pid_auth=pid_auth,
            country_selection=country_selection,
            redirect_url=redirect_url,
        )

    return jsonify({"status": "error", "message": "Payload not found"}), 400


@frontend.route("/display_countries", methods=["POST"])
def display_countries():
    raw_json_string = request.form.get("payload")

    logger.info(f"raw_json_string: {raw_json_string}")

    if raw_json_string:
        try:

            data_payload = json.loads(raw_json_string)
            logger.info(f"data_payload: {data_payload}")

        except json.JSONDecodeError:
            return jsonify({"status": "error", "message": "Invalid JSON payload"}), 400

        session_id = data_payload.get("session_id")
        logger.info(f"session_id: {session_id}")
        countries = data_payload.get("countries")
        logger.info(f"countries: {countries}")

        return render_template(
            "dynamic/dynamic-countries.html",
            countries=countries,
            session_id=session_id,
            redirect_url=CONFIGURATION["backend_url"],
        )

    return jsonify({"status": "error", "message": "Payload not found"}), 400


@frontend.route("/display_form", methods=["POST"])
def display_form():
    raw_json_string = request.form.get("payload")

    if raw_json_string:
        try:
            data_payload = json.loads(raw_json_string)

        except json.JSONDecodeError:
            return jsonify({"status": "error", "message": "Invalid JSON payload"}), 400

        session_id = data_payload.get("session_id")
        logger.info(f"session_id: {session_id}")
        mandatory_attributes = data_payload.get("mandatory_attributes")
        logger.info(f"mandatory_attributes: {mandatory_attributes}")
        optional_attributes = data_payload.get("optional_attributes")
        logger.info(f"optional_attributes: {optional_attributes}")
        redirect_url = data_payload.get("redirect_url")
        logger.info(f"redirect_url: {redirect_url}")

        return render_template(
            "dynamic/dynamic-form.html",
            mandatory_attributes=mandatory_attributes,
            optional_attributes=optional_attributes,
            redirect_url=redirect_url,
        )

    return jsonify({"status": "error", "message": "Payload not found"}), 400


@frontend.route("/display_authorization", methods=["POST"])
def display_authorization():
    raw_json_string = request.form.get("payload")

    if raw_json_string:
        try:
            data_payload = json.loads(raw_json_string)

        except json.JSONDecodeError:
            return jsonify({"status": "error", "message": "Invalid JSON payload"}), 400

        session_id = data_payload.get("session_id")
        logger.info(f"session_id: {session_id}")
        presentation_data = data_payload.get("presentation_data")
        logger.info(f"presentation_data: {presentation_data}")
        redirect_url = data_payload.get("redirect_url")
        logger.info(f"redirect_url: {redirect_url}")

        return render_template(
            "dynamic/form_authorize.html",
            presentation_data=presentation_data,
            user_id=session_id,
            redirect_url=redirect_url,
        )

    return jsonify({"status": "error", "message": "Payload not found"}), 400


@frontend.route("/display_pid_login", methods=["POST"])
def display_pid_login():
    raw_json_string = request.form.get("payload")

    if raw_json_string:
        try:
            data_payload = json.loads(raw_json_string)

        except json.JSONDecodeError:
            return jsonify({"status": "error", "message": "Invalid JSON payload"}), 400

        session_id = data_payload.get("session_id")
        logger.info(f"session_id: {session_id}")

        deeplink_url = data_payload.get("deeplink_url")
        logger.info(f"deeplink_url: {deeplink_url}")

        redirect_url = data_payload.get("redirect_url")
        logger.info(f"redirect_url: {redirect_url}")

        qr_img_base64 = data_payload.get("qr_img_base64")
        logger.info(f"qr_img_base64: {qr_img_base64}")

        transaction_id = data_payload.get("transaction_id")
        logger.info(f"transaction_id: {transaction_id}")

        return render_template(
            "openid/pid_login_qr_code.html",
            url_data=deeplink_url,
            qrcode=qr_img_base64,
            presentation_id=transaction_id,
            redirect_url=CONFIGURATION["service_url"],
        )

    return jsonify({"status": "error", "message": "Payload not found"}), 400


@frontend.route("/credential_offer", methods=["GET", "POST"])
def credentialOffer():
    return redirect(
        f"{CONFIGURATION['backend_url']}/credential_offer_choice?frontend_id={CONFIGURATION['frontend_id']}"
    )


@frontend.route("/.well-known/<service>")
def well_known(service):
    if service == "openid-credential-issuer":

        logger.info(f"openid-credential-issuer")

        accept = request.headers.get("Accept", "")
        wants_jwt = "application/jwt" in accept

        if wants_jwt:
            logger.info(f" openid-credential-issuer JWT")
            resp = make_response(signed_metadata, 200)
            resp.headers["Content-Type"] = "application/jwt"
        else:
            logger.info(f" openid-credential-issuer ELSE")
            resp = make_response(oidc_metadata, 200)
            resp.headers["Content-Type"] = "application/json"

        resp.headers["Pragma"] = "no-cache"
        resp.headers["Cache-Control"] = "no-store"

        return resp

    elif service == "oauth-authorization-server":
        logger.info(f"oauth-authorization-server")

        info = {
            "response": openid_metadata,
            "http_headers": [
                ("Content-type", "application/json"),
                ("Pragma", "no-cache"),
                ("Cache-Control", "no-store"),
            ],
        }

        _http_response_code = info.get("response_code", 200)
        resp = make_response(info["response"], _http_response_code)

        for key, value in info["http_headers"]:
            resp.headers[key] = value

        return resp

    elif service == "openid-configuration":
        # _endpoint = current_app.server.get_endpoint("provider_config")
        info = {
            "response": openid_metadata,
            "http_headers": [
                ("Content-type", "application/json"),
                ("Pragma", "no-cache"),
                ("Cache-Control", "no-store"),
            ],
        }

        _http_response_code = info.get("response_code", 200)
        resp = make_response(info["response"], _http_response_code)

        for key, value in info["http_headers"]:
            resp.headers[key] = value

        return resp

    else:
        return make_response("Not supported", 400)


@frontend.route("/internal_error", methods=["POST"])
def display_internal_error():
    raw_json_string = request.form.get("payload")

    if raw_json_string:
        try:
            data_payload = json.loads(raw_json_string)

        except json.JSONDecodeError:
            return jsonify({"status": "error", "message": "Invalid JSON payload"}), 400

        error = data_payload.get("error")
        error_code = data_payload.get("error_code")
        error_type = data_payload.get("error_type")

        return (
            render_template("misc/500.html", error=error, error_code=error_code),
            error_type,
        )

    return jsonify({"status": "error", "message": "Payload not found"}), 400


@frontend.route("/display_revocation_authorization", methods=["POST"])
def display_revocation_authorization():
    raw_json_string = request.form.get("payload")

    if raw_json_string:
        try:
            data_payload = json.loads(raw_json_string)

        except json.JSONDecodeError:
            return jsonify({"status": "error", "message": "Invalid JSON payload"}), 400

        display_list = data_payload.get("display_list")
        revocation_identifier = data_payload.get("revocation_identifier")
        redirect_url = data_payload.get("redirect_url")
        revocation_choice_url = data_payload.get("revocation_choice_url")

        return render_template(
            "misc/revocation_authorization.html",
            display_list=display_list,
            revocation_identifier=revocation_identifier,
            redirect_url=redirect_url,
            revocation_choice_url=revocation_choice_url,
        )

    return jsonify({"status": "error", "message": "Payload not found"}), 400


@frontend.route("/display_revocation_success", methods=["POST"])
def display_revocation_success():
    """raw_json_string = request.form.get("payload")

    if raw_json_string:
        try:
            data_payload = json.loads(raw_json_string)

        except json.JSONDecodeError:
            return jsonify({"status": "error", "message": "Invalid JSON payload"}), 400

        redirect_url = data_payload.get("redirect_url")"""

    return render_template(
        "misc/revocation_success.html",
        redirect_url=CONFIGURATION["service_url"],
    )

    # return jsonify({"status": "error", "message": "Payload not found"}), 400


@frontend.route("/display_credential_offer", methods=["POST"])
def display_credential_offer():
    raw_json_string = request.form.get("payload")

    if raw_json_string:
        try:
            data_payload = json.loads(raw_json_string)

        except json.JSONDecodeError:
            return jsonify({"status": "error", "message": "Invalid JSON payload"}), 400

        redirect_url = data_payload.get("redirect_url")
        # cred = data_payload.get("cred")
        credential_offer_URI = data_payload.get("credential_offer_URI")

        credentialsSupported = oidc_metadata["credential_configurations_supported"]

        credentials = {"sd-jwt vc format": {}, "mdoc format": {}}

        for cred in credentialsSupported:
            credential = credentialsSupported[cred]

            if credential["format"] == "dc+sd-jwt":
                credentials["sd-jwt vc format"].update(
                    {cred: credential["credential_metadata"]["display"][0]["name"]}
                )

            if credential["format"] == "mso_mdoc":
                credentials["mdoc format"].update(
                    {cred: credential["credential_metadata"]["display"][0]["name"]}
                )

        for key in list(credentials):
            if not credentials[key]:
                del credentials[key]

        return render_template(
            "openid/credential_offer.html",
            cred=credentials,
            redirect_url=redirect_url,
            credential_offer_URI=credential_offer_URI,
        )

    return jsonify({"status": "error", "message": "Payload not found"}), 400


@frontend.route("/display_credential_offer_qr_code", methods=["POST"])
def display_credential_offer_qr_code():
    raw_json_string = request.form.get("payload")

    if raw_json_string:
        try:
            data_payload = json.loads(raw_json_string)

        except json.JSONDecodeError:
            return jsonify({"status": "error", "message": "Invalid JSON payload"}), 400

        wallet_dev = data_payload.get("wallet_dev")
        logger.info(f"wallet_dev: {wallet_dev}")
        credential_offer = data_payload.get("credential_offer")
        logger.info(f"credential_offer: {credential_offer}")
        url_data = data_payload.get("url_data")
        logger.info(f"url_data: {url_data}")
        qrcode = data_payload.get("qrcode")
        logger.info(f"qrcode: {qrcode}")
        tx_code = data_payload.get("tx_code")
        logger.info(f"tx_code: {tx_code}")
        code = data_payload.get("code")
        logger.info(f"code: {code}")

        if tx_code and code:
            return render_template(
                "openid/credential_offer_qr_code.html",
                wallet_dev=wallet_dev
                + "?code="
                + code
                + "&tx_code="
                + str(tx_code)
                + "&credential_offer="
                + json.dumps(credential_offer),
                url_data=url_data,
                tx_code=tx_code,
                qrcode=qrcode,
            )
        else:
            return render_template(
                "openid/credential_offer_qr_code.html",
                wallet_dev=wallet_dev
                + "?credential_offer="
                + json.dumps(credential_offer),
                url_data=url_data,
                qrcode=qrcode,
            )

    return jsonify({"status": "error", "message": "Payload not found"}), 400


@frontend.route("/display_revocation_choice", methods=["POST"])
def display_revocation_choice():
    raw_json_string = request.form.get("payload")

    if raw_json_string:
        try:
            data_payload = json.loads(raw_json_string)

        except json.JSONDecodeError:
            return jsonify({"status": "error", "message": "Invalid JSON payload"}), 400

        redirect_url = data_payload.get("redirect_url")
        cred = data_payload.get("cred")

        return render_template(
            "openid/revocation_choice.html",
            cred=cred,
            redirect_url=redirect_url,
        )

    return jsonify({"status": "error", "message": "Payload not found"}), 400


@frontend.route("/display_revocation_qr_code", methods=["POST"])
def display_revocation_qr_code():
    raw_json_string = request.form.get("payload")

    if raw_json_string:
        try:
            data_payload = json.loads(raw_json_string)

        except json.JSONDecodeError:
            return jsonify({"status": "error", "message": "Invalid JSON payload"}), 400

        url_data = data_payload.get("url_data")
        logger.info(f"url_data: {url_data}")
        qrcode = data_payload.get("qrcode")
        logger.info(f"qrcode: {qrcode}")
        presentation_id = data_payload.get("presentation_id")
        logger.info(f"presentation_id: {presentation_id}")
        redirect_url = data_payload.get("redirect_url")
        logger.info(f"redirect_url: {redirect_url}")

        return render_template(
            "openid/revocation_qr_code.html",
            url_data=url_data,
            qrcode=qrcode,
            presentation_id=presentation_id,
            redirect_url=redirect_url,
        )

    return jsonify({"status": "error", "message": "Payload not found"}), 400
