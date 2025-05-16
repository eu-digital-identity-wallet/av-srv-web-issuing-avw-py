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

This config_countries.py contains configuration data related to the countries supported by the Age Verification Service. 

NOTE: You should only change it if you understand what you're doing.
"""

from .config_service import ConfService as cfgserv


class ConfCountries:
    formCountry = "AV"
    # supported countries
    supported_countries = {
        formCountry: {
            "name": "FormEU",
            "privkey": "/etc/eudiw/age_verification/privKey/AgeVerificationDS-001.pem",
            "privkey_passwd": None,  # None or bytes
            "cert": "/etc/eudiw/age_verification/cert/AgeVerificationDS-001_cert.der",
            "un_distinguishing_sign": "AV",
            "supported_credentials": [
                "eu.europa.ec.eudi.age_verification_mdoc",
            ],
            "dynamic_R2": cfgserv.service_url + "dynamic/form_R2",
        },
        "PT": {
            "name": "Portugal",
            "privkey": "/etc/eudiw/age_verification/privKey/AgeVerificationDS-0001_PT.pem",
            "privkey_passwd": None,  # None or bytes
            "cert": "/etc/eudiw/age_verification/cert/AgeVerificationDS-0001_PT_cert.der",
            "un_distinguishing_sign": "P",
            "supported_credentials": [
            ],
            "connection_type": "oauth",
            "oidc_auth": {
                "url": "https://preprod.autenticacao.gov.pt/oauth/askauthorization?",
                "redirect_uri": cfgserv.service_url + "dynamic/redirect",
                "scope": {
                    "eu.europa.ec.agev10n": {
                        #"given_name": "http://interop.gov.pt/MDC/Cidadao/NomeProprio",
                        #"family_name": "http://interop.gov.pt/MDC/Cidadao/NomeApelido",
                        "birth_date": "http://interop.gov.pt/MDC/Cidadao/DataNascimento",
                        #"nationality": "http://interop.gov.pt/MDC/Cidadao/Nacionalidade",
                        #"birth_place":"http://interop.gov.pt/IMTT/Cidadao/LocalNascimento",
                        #"nif":"http://interop.gov.pt/MDC/Cidadao/NIF"
                        
                    },
                    "org.iso.18013.5.1.mDL": {
                        "nif": "http://interop.gov.pt/MDC/Cidadao/NIF",
                        "birth_date": "http://interop.gov.pt/MDC/Cidadao/DataNascimento",
                        "given_name": "http://interop.gov.pt/IMTT/Cidadao/NomeProprio",
                        "family_name": "http://interop.gov.pt/IMTT/Cidadao/NomeApelido",
                        "issuing_authority": "http://interop.gov.pt/IMTT/Cidadao/EntidadeEmissora",
                        "document_number": "http://interop.gov.pt/IMTT/Cidadao/NoCarta",
                        "portrait": "http://interop.gov.pt/DadosCC/Cidadao/Foto",
                        "driving_privileges": "http://interop.gov.pt/IMTT/Cidadao/Categorias",
                    },
                },
                "response_type": "token",
                "client_id": "8060676576749345306",
            },
            "attribute_request": {
                "url": "https://preprod.autenticacao.gov.pt/oauthresourceserver/api/AttributeManager?token=",
                "headers": "",
                "custom_modifiers": "",
            },
        },
    }
