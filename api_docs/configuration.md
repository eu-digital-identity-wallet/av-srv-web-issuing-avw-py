# Configuration

For configuring your locally installed version of the EUDIW Issuer Front-end, you need to change the following configurations.

## 1. Service Configuration

Base configuration example for the EUDIW Issuer Front-end is located in ```frontend_config_example.yaml```.

Parameters that should be changed:

- `service_url` (Base url of the service)
- `frontend_id` (The front-end id registered in the backend service)
- `backend_url` (Base url for the back-end service)
- `oauth_url` (Base url for the authorization service)
- `credentials_supported` (Credentials supported by this front-end)
- `log_dir` (Log directory)
