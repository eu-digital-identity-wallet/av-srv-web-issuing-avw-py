# Pre-authorized

For the pre-authorized flow, you can test our examples by selecting Pre-Authorization Code Grant in https://issuer.ageverification.dev/credential_offer (or <https://localhost/credential_offer> if installed locally).

After submitting, a QR code, transaction code and DeepLink are generated:

   ![image](images/pre-auth_qr.png)

```
openid-credential-offer://credential_offer?credential_offer=%7B%22credential_issuer%22:%20%22https://issuer.ageverification.dev%22%2C%20%22credential_configuration_ids%22:%20%5B%22eu.europa.ec.eudi.age_over18_mdoc%22%5D%2C%20%22grants%22:%20%7B%22urn:ietf:params:oauth:grant-type:pre-authorized_code%22:%20%7B%22pre-authorized_code%22:%20%229199e901-ba33-4ef4-911b-2f44a824049e%22%2C%20%22tx_code%22:%20%7B%22length%22:%205%2C%20%22input_mode%22:%20%22numeric%22%2C%20%22description%22:%20%22Please%20provide%20the%20one-time%20code.%22%7D%7D%7D%7D
```
   
