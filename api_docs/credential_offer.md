# Credential Offer 

## 1. Authorization code flow
 
**Endpoint**: <https://issuer.ageverification.dev/credential_offer> (or <https://localhost/credential_offer> if installed locally)

A form is presented showing the Request Credentials for your Age Verification Wallet that can be requested.

![image](images/credential_offer.png)

After choosing the credential(s) and submitting, a QR code and DeepLink is generated:

![image](images/credential_offer_qr.png)

This generated DeepLink contains information about the credentials chosen in the form.

 **Example:**

   if the selected options are Personal Identification Data and the Mobile Driver's License in both sd-jwt and mdoc format:

```
openid-credential-offer://credential_offer?credential_offer=%7B%22credential_issuer%22:%20%22https://issuer.ageverification.dev%22%2C%20%22credential_configuration_ids%22:%20%5B%22eu.europa.ec.eudi.age_over18_mdoc%22%5D%2C%20%22grants%22:%20%7B%22authorization_code%22:%20%7B%7D%7D%7D
```


## 2. Pre-Authorized Code Flow

**Endpoint**: <https://dev.issuer.ageverification.dev/dynamic/preauth> (or <https://localhost/dynamic/preauth> if installed locally)


Example of generated DeepLink:
```
openid-credential-offer://credential_offer?credential_offer=%7B%22credential_issuer%22:%20%22https://issuer.ageverification.dev%22%2C%20%22credential_configuration_ids%22:%20%5B%22eu.europa.ec.eudi.age_over18_mdoc%22%5D%2C%20%22grants%22:%20%7B%22urn:ietf:params:oauth:grant-type:pre-authorized_code%22:%20%7B%22pre-authorized_code%22:%20%229199e901-ba33-4ef4-911b-2f44a824049e%22%2C%20%22tx_code%22:%20%7B%22length%22:%205%2C%20%22input_mode%22:%20%22numeric%22%2C%20%22description%22:%20%22Please%20provide%20the%20one-time%20code.%22%7D%7D%7D%7D
```
