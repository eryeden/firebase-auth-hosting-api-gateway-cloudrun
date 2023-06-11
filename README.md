# firebase-auth-hosting-api-gateway-cloudrun

This repository is dedicated to accomplishing the following features:

- API authentification using API Gateway in GCP
- Frontend hosting using Firebase hosting
- Login page by Firebase auth UI
- User-specific page
    - User name
    - User ID
- Restricted message; Only authorized users have access to this message.
  General page
- The greeting message that accessible to all users.
- FastAPI backend using GCP Cloud-Run

FastAPI has the following API endpoints:

- **Authentication required:**
    - /user_info; user id, user name
    - /special_message; "You are special!"
- **Authentication not required:**
    - /greeting_message; "Welcome back, sir!"

Authentification

## Architecture

The system architecture is shown in the figure below:
![fig](docs/arch_design.drawio.png)

## Task

- [x] Construct the FastAPI backend
- [x] Deploy the FastAPI backend on CloudRun
- [x] Configure the API gateway(The step1 box in the arch fig.)
- [ ] Build the frontend side; We will prepare the frontend side for the test purpose.
- [ ] Test the API access with authorization

## Project memo

### Construct the FastAPI backend

Python environment setup:

```bash
pyenv local 3.11.3
python -m venv .venv
poetry init
poetry shell
poetry add fastapi[all] firebase_admin urllib3==1.26.15
poetry export -f requirements.txt --output requirements.txt
```

Prepare the Dockerfile: [Dockerfile](./Dockerfile)

### Prepare Firebase/GCP project

I have prepared the following service:

| Name                    | Parameter            | Description                      |
|-------------------------|----------------------|----------------------------------|
| Firebase project        | Project name: FAHAGC | Project of Firebase              |
| GCP project             | Project name: FAHAGC | Use the same project as firebase |
| GCP Cloud Run           | NA                   | For hosting the API backend      |
| GCP API Gateway         | NA                   | For API authorization            |
| Secret Manager API      | NA                   | For credential management        |
| Firebase authentication | NA                   | For user authorization           |
| Firebase auth UI        | NA                   | For user login screen            |

#### Details for GCP/Firebase project

| Parameter        | Value           | Description             |
|------------------|-----------------|-------------------------|
| Project name     | fahagc          | NA                      |
| PROJECT_ID       | fahagc-c908b    | NA                      |
| Region           | asia-northeast1 | The region in Japan     |
| API gateway name | fahagc-backend  | The name of API gateway |

### Secret management

In this project, a Secret manager is used for secret management.
I uploaded `firebase_credentials.json` on the GCP Secret manager. FastAPI can access this secret and load this file by
accessing `/secret/firebase_test_secret`.
The path to the secret file can be configured on the GCP console.
FastAPI can get he path to the secret file via an environment varibale `PATH_TO_FIREBASE_CREDENTIALS`. If the env var is
not defined, FastAPI will use the default path `"./backend_app/firebase_credentials.json"`.

### Deploy to the Cloud Run

The following command will deploy the backend built by FastAPI.
The deployment will fail if the current service account cannot access the secret manager.
Open the console of CloudRun service and give a privilege to the current service account to solve this problem.

```bash
gcloud init
gcloud config set project PROJECT_ID
gcloud config set run/region asia-northeast1
gcloud run deploy firebase-auth-hosting-api-gateway-cloudrun \
--set-env-vars "PATH_TO_FIREBASE_CREDENTIALS=/secret/firebase_test_secret" \
--set-secrets=/secret/firebase_test_secret=firebase_test_secret:latest \
--source .
```

`PROJECT_ID` is CloudRun's project id like; `fahagc-c908b`.
You can tune the location to deploy by changing `asia-northeast1`.

### Setting up API gateway

#### Parameters for API gateway

| Parameter             | Value                                                                      |
|-----------------------|----------------------------------------------------------------------------|
| PROJECT_ID            | fahagc-c908b                                                               |
| API_ID                | fahagc-backend                                                             |
| APP_URL               | https://firebase-auth-hosting-api-gateway-cloudrun-4lvq7hntvq-an.a.run.app |
| CONFIG_ID             | fahagc-backend-config                                                      |
| SERVICE_ACCOUNT_EMAIL | 967712212023-compute@developer.gserviceaccount.com                         |
| GATEWAY_ID            | fahagc-backend-gateway                                                     |
| GCP_REGION            | asia-northeast1                                                            |

1. Enable API gateway services:

```bash
gcloud services enable apigateway.googleapis.com
gcloud services enable servicemanagement.googleapis.com
gcloud services enable servicecontrol.googleapis.com
```

2. Crate the API:

```bash
gcloud api-gateway apis create fahagc-backend
```

`fahagc-backend` should be a name of API.

3. Define the API specification:
   [here](api_gateway/openapi2-api-backend.yaml)


4. Configure the API gateway
   This command configures API.

```bash
gcloud api-gateway api-configs create fahagc-backend-config \
  --api=fahagc-backend --openapi-spec=api_gateway/openapi2-api-backend.yaml \
  --project=fahagc-c908b --backend-auth-service-account=967712212023-compute@developer.gserviceaccount.com
```

5. Deployment
   This command will deploy the api gateway. The configuration will be mapped by `api-config` id.

```bash
gcloud api-gateway gateways create fahagc-backend-gateway \
  --api=fahagc-backend --api-config=fahagc-backend-config \
  --location=asia-northeast1 --project=fahagc-c908b
```

At this point, the API gateway without authorization will be realized.
I will proceed to implement the API gateway with authorization functionality.

6. Add the authorization functionality:

You can add the authentication feature using the following configuration:

```yaml
# Configurations for the API authorization
securityDefinitions:
  firebase:
    authorizationUrl: ""
    flow: "implicit"
    type: "oauth2"
    # Replace YOUR-PROJECT-ID with your project ID
    x-google-issuer: "https://securetoken.google.com/fahagc-c908b"
    x-google-jwks_uri: "https://www.googleapis.com/service_accounts/v1/metadata/x509/securetoken@system.gserviceaccount.com"
    x-google-audiences: "fahagc-c908b"
```

You should write the above configuration on the top level
of [yaml specification](api_gateway/openapi2-api-backend.yaml).

### The frontend

I will prepare the front end beforehand for testing the API gateway.
The followings are used for this front end:

| Name | Description        |
|------|--------------------|
| vue3 | Frontend framework |
| Vite | Frontend tooling   |

```bash
npm init vue@latest
cd vue-frontend
npm install axios vue-axios firebaseui firebase-tools
npm run dev
```






