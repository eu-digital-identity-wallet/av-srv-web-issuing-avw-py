# coding: latin-1
###############################################################################
# Copyright (c) 2023 European Commission
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
###############################################################################
"""
The PID Issuer Web service is a component of the PID Provider backend.
Its main goal is to issue the PID and MDL in cbor/mdoc (ISO 18013-5 mdoc) and SD-JWT format.


This misc.py file includes different miscellaneous functions.
"""

# Standard library imports
import base64
import datetime
import json
import secrets
import uuid
from io import BytesIO
from typing import Any, Dict, Optional, Tuple

# Third-party imports
import jwt
from cryptography import x509
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.asymmetric.types import CertificatePublicKeyTypes
from PIL import Image
from flask import current_app, jsonify, redirect
from flask.helpers import make_response

# Local/project-specific imports
from app import oidc_metadata
from app import trusted_CAs
from redirect_func import url_get


def urlsafe_b64encode_nopad(data: bytes) -> str:
    """
    Encodes bytes using URL-safe base64 and removes padding.

    Args:
        data (bytes): The data to encode.

    Returns:
        str: Base64 URL-safe encoded string without padding.
    """
    return base64.urlsafe_b64encode(data).decode("utf-8").rstrip("=")


def b64url_decode(data: str) -> bytes:
    """Decode base64url encoded data with proper padding."""
    padding = "=" * (-len(data) % 4)
    return base64.urlsafe_b64decode(data + padding)
