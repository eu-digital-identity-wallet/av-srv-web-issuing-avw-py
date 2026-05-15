# Installation

## 1. Python

The Age Verification (AV) Issuer was tested with

+ Python version 3.13

and should only be used with Python 3.10+.

If you don't have it installed, please download it from <https://www.python.org/downloads/> and follow the [Python Developer's Guide](https://devguide.python.org/getting-started/).

## 2. Flask

The AV Issuer was tested with

+ Flask v. 3.1

and should only be used with Flask v. 3.1 or higher.

To install [Flask](https://flask.palletsprojects.com/en/stable/), please follow the [Installation Guide](https://flask.palletsprojects.com/en/stable/installation/).

+ NPM 10.6.0
+ NodeJS v20.12.2

To install [NPM](https://docs.npmjs.com/), please follow the [Installation Guide](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm).

## 3. How to run the AV Issuer Front End?

To run the AV Issuer Front End, please follow these simple steps (some of which may have already been completed when installing Flask) for Linux/macOS or Windows.


1. Clone the AV Issuer repository:

    ```shell
    git clone git@github.com:eu-digital-identity-wallet/av-srv-web-issuing-avw-py.git
    ```

2. Create a `.venv` folder within the cloned repository:

    ```shell
    cd av-srv-web-issuing-avw-py
    python3 -m venv .venv
    ```

3. Activate the environment:

   Linux/macOS

    ```shell
    . .venv/bin/activate
    ```

    Windows

    ```shell
    . .venv\Scripts\Activate
    ```


4. Install or upgrade _pip_

    ```shell
    python -m pip install --upgrade pip
    ```


5. Install Flask, gunicorn and other dependencies in virtual environment

    ```shell
    pip install -r app/requirements.txt
    ```

6. Setup config
   
   -  Copy ```.frontend_config_example.yaml``` to ```etc/issuer_config/frontend_config_example.yaml``` and modify variables.

   ```shell
   cp .frontend_config_example.yaml etc/issuer_config/frontend_config_example.yaml
   ```
   Configuration location can be changed using environment variable ISSUER_CONFIG_PATH

7. Service Configuration

   - Configure the service according to [documentation](api_docs/configuration.md)  

8. NPM build
    ```shell
    npm install
    ```

    ```shell
    npm run build
    ```

9. Install Authorization Server
    - Install the service according to [Issuer Authorization Server](https://github.com/eu-digital-identity-wallet/eudi-srv-issuer-oidc-py/blob/main/install.md)

10. Install Issuer Back End
    - Install the service according to [Issuer Back End](https://github.com/eu-digital-identity-wallet/eudi-srv-web-issuing-eudiw-py/blob/main/install.md)

11. Run the AV Issuer Front End

    The Issuer Back End and Authorization Server should be running beforehand.

    On the root directory of the clone repository, insert one of the following command lines to run the AV Issuer Front End.

    + Linux/macOS/Windows (on <http://127.0.0.1:5000> or <http://localhost:5000>)

    ```
    flask --app app run
    ```

    + Linux/macOS/Windows (on <http://127.0.0.1:5000> or <http://localhost:5000> with flag debug)

    ```
    flask --app app run --debug
    ```

    
## 5. Make your local AV Issuer Front End available on the Internet (optional)

If you want to make your local AV Issuer available on the Internet, we recommend to use NGINX reverse proxy and certbot (to generate an HTTPS certificate).

### 5.1 Install and configure NGINX

1. Follow the installation guide in https://docs.nginx.com/nginx/admin-guide/web-server/reverse-proxy/

2. Configure your local AV Issuer. For example, use the following Nginx configuration file (for a Linux installation):

```nginx
server {
    server_name FQDN; # Change to the FQDN you want to use

    listen 80;
    access_log /var/log/nginx/issuer.av.access.log;
    error_log /var/log/nginx/issuer.av.error.log;
    root /var/www/html;

# Recommended
    proxy_busy_buffers_size   512k;
    proxy_buffers   4 512k;
    proxy_buffer_size   256k;

# Provider backend
    location / {
        # The proxy_pass directive assumes that your local AV Issuer is running at http://127.0.0.1:5000/. 
        # If not, please adjust it accordingly.
        proxy_pass                              http://127.0.0.1:5000/;
        proxy_set_header Host                   $http_host;
        proxy_set_header X-Real-IP              $remote_addr;
        proxy_set_header X-Forwarded-For        $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto      $scheme;
    }
}
```

3. Restart the Nginx server


### 5.2 Install and run certbot to gef a free HTTPS certificate

1. Follow the installation guide in https://certbot.eff.org

2. Run `certbot` to get a free HTTPS certificate. The `certbot` will also configure the AV Issuer Nginx configuration file with the HTTPS certificate.

3. Restart the Nginx server and goto `https:\\FQDN\` (FQDN configured in the Nginx configuration file)


## 6. Docker

This guide provides step-by-step instructions for deploying the **AV Issuer** service using **Docker Compose v2**.

1. Install docker

    Ensure you have Docker installed on your system. Follow the **official installation instructions** for your operating system:
    [https://docs.docker.com/engine/install/](https://docs.docker.com/engine/install/)


2. Deploy Related Services

To complete the full AV ecosystem, you will need to deploy the associated Authorization server and Back-end components if you haven't already.

* **Back-end Installation:** Follow the guide to install the back-end component using Docker.
    * [Back-end Deployment Guide](https://github.com/eu-digital-identity-wallet/eudi-srv-web-issuing-eudiw-py/blob/main/install.md#6-docker)

* **Authorization Server Installation:** Follow the guide to install the OIDC authorization server component using Docker.
    * [Authorization Server Deployment Guide](https://github.com/eu-digital-identity-wallet/eudi-srv-issuer-oidc-py/blob/main/install.md#6-docker)

3. Configure Docker Compose

    The service's container orchestration is managed by the `docker-compose.yml` file.

    * **Customize the configuration:** Review and modify the local `docker-compose.yml` file to align with your specific deployment requirements (e.g., exposed ports, service names, volumes).
    * *Reference file:* [docker-compose.yml](./docker-compose.yml)

4. Set Up Configuration

    Service parameters and sensitive settings are managed through a configuration file.

    * **Create the configuration file:** We recommend copying the example file to create your local configuration.

    * **Update variables:** Edit the newly created `frontend_config_example.yaml` file with your specific settings and credentials.
        * *Reference example:* [frontend_config_example.yaml](frontend_config_example.yaml)


5. Pull the Docker Image

    ```
    docker compose pull
    ```

6. Run the 

    Start the AV Issuer backend in detached mode (runs in the background):

    ```
    docker compose up -d
    ```

7. Check Logs

    To confirm the service is running correctly and to monitor its output in real-time for troubleshooting, use the following command:
    ```
    docker compose logs -f
    ```

