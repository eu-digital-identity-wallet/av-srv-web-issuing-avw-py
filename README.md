<!--
SPDX-FileCopyrightText: 2025 European Commission

SPDX-License-Identifier: Apache-2.0
-->

![Proof of age attestations for all Europeans - An age verification solution for EU citizens and residents](images/top-banner-av.png)


# Age Verification Issuer Front End

[![License](https://img.shields.io/badge/License-Apache%202.0-green.svg?style=flat)](https://www.apache.org/licenses/LICENSE-2.0)
[![Last Commit](https://img.shields.io/github/last-commit/eu-digital-identity-wallet/av-app-android-wallet-ui?style=flat)](/../../commits)
[![Open Issues](https://img.shields.io/github/issues/eu-digital-identity-wallet/av-app-android-wallet-ui?style=flat)](/../../issues)

**Important!** Before you proceed, please read
the [Age Verification Solution Technical Specification](https://github.com/eu-digital-identity-wallet/av-doc-technical-specification)


### Overview

The Age Verification (AV) Issuer Front End is an implementation of a (Q)EAA Provider service, following the [Age Verification Specification](https://ageverification.dev/Technical%20Specification/architecture-and-technical-specifications/). It is based on release 0.9.4 of the [EUDI Issuer Front End](https://github.com/eu-digital-identity-wallet/eudi-srv-web-issuing-frontend-eudiw-py) and requires the setup of [EUDI Issuer Back End](https://github.com/eu-digital-identity-wallet/eudi-srv-web-issuing-eudiw-py) as well as 
[EUDI Issuer Authorization Server](https://github.com/eu-digital-identity-wallet/eudi-srv-issuer-oidc-py).


The service provides support for the `mso_mdoc` format of the "Proof of Age" attestation with the namespace “eu.europa.ec.av.1”.

For authenticating the user, it requires the use of eIDAS node, OAUTH2 server or a simple form (for testing purposes).

You can use the Age Verification Issuer at https://issuer.ageverification.dev/, or install it locally (see [installation instructions](#1-installation))
                                                      |


### AV profile coverage
The following is the coverage according to the [Age Verification Specification](https://ageverification.dev/Technical%20Specification/architecture-and-technical-specifications/).


| Feature                                                   | Coverage                                                        |
|-------------------------------------------------------------------|-----------------------------------------------------------------|
| [Authorization Code flow](https://github.com/eu-digital-identity-wallet/eudi-srv-issuer-oidc-py/blob/main/api_docs/authorization.md)        | ✅ Support for scoped                                           |
| [Pre-authorized code flow](https://github.com/eu-digital-identity-wallet/av-srv-web-issuing-avw-py/blob/main/api_docs/pre-authorized.md)            | ✅                                                              |
| [Credential Offer](https://github.com/eu-digital-identity-wallet/av-srv-web-issuing-avw-py/blob/main/api_docs/credential_offer.md)                  | ✅ `authorization_code` , ✅ `pre-authorized_code`              |
| mso_mdoc format                                                   | ✅                                                              |
| [Token Endpoint](https://github.com/eu-digital-identity-wallet/eudi-srv-issuer-oidc-py/blob/main/api_docs/token.md)                               | ✅                                                              |
| [Credential Endpoint](https://github.com/eu-digital-identity-wallet/eudi-srv-web-issuing-eudiw-py/blob/main/api_docs/credential.md)                     | ✅                                                              |
| Credential Issuer Metadata                                        | ✅ Unsigned metadata / Signed Metadata                                           | 
| [Nonce endpoint](https://github.com/eu-digital-identity-wallet/eudi-srv-web-issuing-eudiw-py/blob/main/api_docs/nonce_endpoint.md)                      | ✅                                                              | 
| [Deferred Endpoint](https://github.com/eu-digital-identity-wallet/eudi-srv-web-issuing-eudiw-py/blob/main/api_docs/deferred.md)                         | ✅ Encryption support                                           |
| Proof                                                             | ✅ JWT, Key Attestations                                        |
| Credential response encryption                                    | ✅                                                              |
| Credential request encryption                                     | ✅                                                              |
| Pushed authorization request (PAR)                                     | ✅                                                              |
| Wallet authentication                                             | ✅ public client, Wallet client attestations                    |
| Demonstrating Proof of Possession (DPoP)                          | ✅                                                              |
| PKCE                                                              | ✅                                                              |


Additional coverage can be found at [OpenId4VCI coverage](https://github.com/eu-digital-identity-wallet/eudi-srv-web-issuing-eudiw-py#openid4vci-coverage).

## 1. Installation

You can use the Age Verification Issuer at https://issuer.ageverification.dev/, or install it locally by following the instructions in this section.

## 1. Installation

Pre-requisites:

+ Python v. 3.10+
+ Flask v. 3.1
+ NPM 10.6.0
+ NodeJS v20.12.2

Click [here](install.md) for detailed installation instructions.


## 2. Run

Click [here](install.md) for detailed instructions.

## 3. Frequently Asked Questions

### A. Can I configure my local Age Verification Issuer Front End so that it is available on the Internet?

Please see detailed instructions on how to make your [local AV Issuer available on the Internet install.md](./install.md#5-make-your-local-av-issuer-front-end-available-on-the-internet-optional), and on how to get a [free HTTPS certificate](./install.md#52-install-and-run-certbot-to-gef-a-free-https-certificate).

### B. Can I use my IACA certificate with the Age Verification Issuer?

Yes. You must copy your IACA trusted certificate(s) (in PEM format) to the `trusted_CAs_path` folder. If you don't have an IACA certificate, we provide an example test IACA certificate for the country AgeVerification (AV).

See more information in [issuer backend configuration](https://github.com/eu-digital-identity-wallet/eudi-srv-web-issuing-eudiw-py/blob/main/app/config_issuer_backend_example.yaml).

### C. Can I use my Document Signer private key and certificate with the Age Verification Issuer?

Yes. Please follow the instructions in [issuer backend configuration](https://github.com/eu-digital-identity-wallet/eudi-srv-web-issuing-eudiw-py/blob/main/app/config_issuer_backend_example.yaml). If you don't have Document Signer private key and certificate, we provide  test private DS keys and certificates, for country AgeVerification (AV).

### D. Can I run the issuer in a Docker container?

Yes. Please see how in [Install Docker](install.md#6-docker).

### E. Where can I find the IACA certificate?
The IACA included in a trusted list can be found at [api_docs/test_tokens/IACA-token/AgeVerificationIssuer.IACA.01.EU.pem](api_docs/test_tokens/IACA-token/AgeVerificationIssuer.IACA.01.EU.pem)

## Support and feedback

The following channels are available for discussions, feedback, and support requests:

| Type                     | Channel                                                |
| ------------------------ | ------------------------------------------------------ |
| **Issues**    | <a href="/../../issues" title="Open Issues"><img src="https://img.shields.io/github/issues/eu-digital-identity-wallet/av-verifier-ui?style=flat"></a>  |
| **Discussion**    | <a href="https://github.com/eu-digital-identity-wallet/av-doc-technical-specification/discussions" title="Discussion"><img src="https://img.shields.io/github/discussions/eu-digital-identity-wallet/av-doc-technical-specification"></a>  |
| **Other requests**    | <a href="mailto:av-tscy@scytales.com" title="Email AVS Team"><img src="https://img.shields.io/badge/email-AVS%20team-green?logo=mail.ru&style=flat-square&logoColor=white"></a>   |

## Important note

This white-label application is a reference implementation of the Age Verification solution that should be customised before publishing it. The current version is not feature complete and will require further integration work before production deployment. In particular, any national-specific enrolment procedures must be implemented by the respective Member States or publishing parties.

Please note that this application is still under active development. It is regularly updated and new features and improvements are continuously being added.


## How to contribute

We welcome contributions to this project. To ensure that the process is smooth for everyone
involved, follow the guidelines found in [CONTRIBUTING.md](CONTRIBUTING.md).

## Code of Conduct

This project has adopted the [Contributor Covenant](https://www.contributor-covenant.org/) in version 2.1 as our code of conduct. Please see the details in our [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md). All contributors must abide by the code of conduct.

By participating in this project, you agree to abide by its [Code of Conduct](CODE_OF_CONDUCT.md) at all times.

### License details

Copyright (c) 2025 European Commission

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
