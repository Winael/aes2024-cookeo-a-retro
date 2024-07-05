# Le Cookeo à Rétro by Zenika

Le Cookéo à Rétro by Zenika est une application permettant de créér facilement des rétrospectives agiles originales grâce à la puissance de l'IA Générative.

## Construire l'image docker

Pour contruire l'image docker en local :

```sh
docker build -t aes2024-cookeo-a-retro .
```

Pour tester localement l'image docker :

```sh
docker run -p 5000:5000 aes2024-cookeo-a-retro
```

## CI/CD avec Github Actions

Pour pouvoir associer des workloads à Google Cloud, il est nécessaire de passer maintenant par un pool d'identité de workload et de lui associé un fournisseur (pour plus d'information, voir la vidéo [ici](https://www.youtube.com/watch?v=ZgVhU5qvK1M))

```sh
export SERVICE_ACCOUNT="github-actions-service-account"
export WORKLOAD_IDENTITY_POOL_NAME="github-pool"
export DOCKER_REPO="docker-repo"
export GITHUB_ORG="Zenika"
export LOCATION="europe-west1"
export WORKLOAD_IDENTITY_PROVIDER_NAME="github-actions-provider"
```

### Création du dépôt pour les images Docker sur Artifact Registry

```sh
gcloud artifacts repositories create ${DOCKER_REPO} \
    --project=${PROJECT_ID} \
    --repository-format=docker \
    --location=europe-west1 \
    --description="Dépôt Docker"
```

### Création du Pool d'identité pour Github

1. Création du Service Account `github-actions-service-account`:

```sh
gcloud iam service-accounts create ${SERVICE_ACCOUNT} \
 --description="A service account for use in a GitHub Actions workflow" \
 --display-name="GitHub Actions service account."
```

2. Ajout de la police d'accès `roles/artifactregistry.createOnPushWriter` au service account :

```sh
gcloud artifacts repositories add-iam-policy-binding ${DOCKER_REPO} \
  --project=${PROJECT_ID} \
  --location=${LOCATION} \
  --role=roles/artifactregistry.createOnPushWriter \
  --member=serviceAccount:${SERVICE_ACCOUNT}@${PROJECT_ID}.iam.gserviceaccount.com
```

3. Création du Pool d'identité `github-pool` pour Github :

```sh
gcloud iam workload-identity-pools create "${WORKLOAD_IDENTITY_POOL_NAME}" \
  --project="${PROJECT_ID}" \
  --location="global" \
  --display-name="GitHub Actions Identity Pool"
```

```sh
export WORKLOAD_IDENTITY_POOL=$( \
  gcloud iam workload-identity-pools describe "github-pool" \
    --project="${PROJECT_ID}" \
    --location="global" \
    --format="value(name)" \
)
```

4. Création du fournisseur pour Github :

```sh
gcloud iam workload-identity-pools providers create-oidc "${WORKLOAD_IDENTITY_PROVIDER_NAME}" \
  --project="${PROJECT_ID}" \
  --location="global" \
  --workload-identity-pool="${WORKLOAD_IDENTITY_POOL_NAME}" \
  --display-name="Provider for GitHub Actions" \
  --issuer-uri="https://token.actions.githubusercontent.com" \
  --attribute-mapping="google.subject=assertion.sub,attribute.actor=assertion.actor,attribute.repository=assertion.repository,attribute.repository_owner=assertion.repository_owner" \
  --attribute-condition="assertion.repository_owner == '${GITHUB_ORG}'"
```

5. Ajout des police d'accès au pool d'identité pour Github :

- `roles/iam.workloadIdentityUser`

```sh
gcloud iam service-accounts add-iam-policy-binding "${SERVICE_ACCOUNT}@${PROJECT_ID}.iam.gserviceaccount.com" \
  --project="${PROJECT_ID}" \
  --role="roles/iam.workloadIdentityUser" \
  --member="principalSet://iam.googleapis.com/${WORKLOAD_IDENTITY_POOL}/attribute.repository/docker-repo"
```

- `roles/iam.workloadIdentityTokenCreator`

```sh
gcloud iam service-accounts add-iam-policy-binding "${SERVICE_ACCOUNT}@${PROJECT_ID}.iam.gserviceaccount.com" \
  --project="${PROJECT_ID}" \
  --role="roles/iam.serviceAccountTokenCreator" \
  --member="principalSet://iam.googleapis.com/${WORKLOAD_IDENTITY_POOL}/attribute.repository/docker-repo"