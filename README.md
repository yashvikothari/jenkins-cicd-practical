# Jenkins CI/CD Practical

This repository demonstrates a Jenkins CI/CD pipeline for a small Python HTTP application.

## Pipeline stages

1. Checkout
2. Build
3. Test
4. Package
5. Build Docker Image
6. Push Docker Image

## Run the app locally

```bash
APP_NAME="Jenkins CI/CD Demo" APP_ENV=local PORT=8080 python3 src/app.py
```

Open:

- http://localhost:8080/
- http://localhost:8080/health

## Run automated tests

```bash
python3 -m unittest discover -s tests -v
```

## Docker

Replace `YOUR_DOCKERHUB_USERNAME` with your Docker Hub username.

```bash
docker build -t YOUR_DOCKERHUB_USERNAME/jenkins-cicd-demo:local .
docker run --rm -p 8080:8080 -e APP_ENV=local YOUR_DOCKERHUB_USERNAME/jenkins-cicd-demo:local
```

## Jenkins requirements

Install/configure:

- Git
- Python 3
- Docker Engine/CLI
- Jenkins Pipeline plugin
- Git plugin
- Credentials Binding plugin

The Jenkins agent that runs this job must be able to invoke Docker.

## Docker Hub credential in Jenkins

Go to:

`Manage Jenkins → Credentials → System → Global credentials → Add Credentials`

Use:

- Kind: Username with password
- Username: your Docker Hub username
- Password: a Docker Hub access token
- ID: `dockerhub-credentials`

Do not commit the token to Git.

## Create the Jenkins pipeline

1. Jenkins → **New Item**
2. Choose **Pipeline**
3. In **Pipeline**, choose **Pipeline script from SCM**
4. SCM: **Git**
5. Repository URL: your GitHub repository URL
6. Branch: `*/main`
7. Script Path: `Jenkinsfile`
8. Save
9. Click **Build Now**

Before the first build, edit `Jenkinsfile` and replace:

`YOUR_DOCKERHUB_USERNAME/jenkins-cicd-demo`

with your actual Docker Hub repository.

## GitHub webhook

If Jenkins is reachable from GitHub:

1. GitHub repository → **Settings → Webhooks → Add webhook**
2. Payload URL: `https://YOUR_JENKINS_HOST/github-webhook/`
3. Content type: `application/json`
4. Select **Just the push event**
5. In Jenkins enable **GitHub hook trigger for GITScm polling**

A Jenkins server available only at `localhost` cannot normally receive GitHub webhooks directly. In that case use manual builds or expose Jenkins through an approved secure tunnel/reverse proxy.

## Screenshots required for submission

Capture these after a real successful run:

1. **Pipeline Screenshot** — stage view showing successful stages.
2. **Successful Build Screenshot** — build page or console output showing `SUCCESS`.
3. **Docker Image Screenshot** — Docker Hub repository page showing `latest` and the numeric Jenkins build tag.
4. **GitHub Repository Link** — copy the URL of the repository containing these files.

## Deployment strategy study

### Blue-Green Deployment

Two matching production environments are maintained: Blue and Green. One serves live traffic while the other receives the new release. After validation, traffic is switched to the new environment. Rollback is fast because traffic can be switched back. The main disadvantage is the extra infrastructure required to keep two environments available.

### Rolling Deployment

Application instances are updated gradually in batches rather than all at once. This keeps the service available during deployment and usually needs less duplicate infrastructure than blue-green. However, old and new versions may temporarily run together, so compatibility and rollback require more planning.
