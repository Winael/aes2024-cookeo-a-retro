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

### Création du dépôt pour les images Docker sur Artifact Registry

```sh
gcloud artifacts repositories create docker-repo \
    --repository-format=docker \
    --location=europe-west1 \
    --description="Dépôt Docker"
```

### Création du Pool d'identité pour Github

1. Création du Service Account `github-actions-service-account`:

```sh
gcloud iam service-accounts create github-actions-service-account \
 --description="A service account for use in a GitHub Actions workflow" \
 --display-name="GitHub Actions service account."
```

2. Ajout de la police d'accès `roles/artifactregistry.createOnPushWriter` au service account :

```sh
gcloud artifacts repositories add-iam-policy-binding docker-repo \
  --location=europe-west1 \
  --role=roles/artifactregistry.createOnPushWriter \
  --member=serviceAccount:github-actions-service-account@aes2024-cookeo-a-retro.iam.gserviceaccount.com
```

3. Création du Pool d'identité `github-pool` pour Github :

```sh
gcloud iam workload-identity-pools create "github-pool" \
  --project="${PROJECT_ID}" \
  --location="global" \
  --display-name="GitHub Actions Identity Pool"
```

```sh
gcloud iam workload-identity-pools describe "github-pool" \
  --project="${PROJECT_ID}" \
  --location="global" \
  --format="value(name)"
projects/663619780066/locations/global/workloadIdentityPools/github-pool
```

4. Création du fournisseur pour Github :

```sh
gcloud iam workload-identity-pools providers create-oidc "github-actions-provider" \
  --project="${PROJECT_ID}" \
  --location="global" \
  --workload-identity-pool="github-pool" \
  --display-name="Provider for GitHub Actions" \
  --issuer-uri="https://token.actions.githubusercontent.com" \
  --attribute-mapping="google.subject=assertion.sub,attribute.actor=assertion.actor,attribute.repository=assertion.repository,attribute.repository_owner=assertion.repository_owner" \
  --attribute-condition="assertion.repository_owner == '${GITHUB_ORG}'"
```

5. Ajout de la police d'accès `roles/iam.workloadIdentityUser` au pool d'identité pour Github :

```sh
gcloud iam service-accounts add-iam-policy-binding "github-actions-service-account@${PROJECT_ID}.iam.gserviceaccount.com" \
  --project="${PROJECT_ID}" \
  --role="roles/iam.workloadIdentityUser" \
  --role="roles/iam.serviceAccountTokenCreator" \
  --member="principalSet://iam.googleapis.com/projects/663619780066/locations/global/workloadIdentityPools/github-pool/attribute.repository/docker-repo"
```
  
         
