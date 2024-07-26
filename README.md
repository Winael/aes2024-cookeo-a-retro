# Le Cookeo à Rétro by Zenika

Le Cookéo à Rétro by Zenika est une application permettant de créér facilement des rétrospectives agiles originales grâce à la puissance de l'IA Générative.

## Construire l'image docker

```sh
export SERVICE_ACCOUNT="github-actions-service-account@${PROJECT_ID}.iam.gserviceaccount.com"
export GAR_LOCATION="europe-west1"
export GAR_REPOSITORY="${GAR_LOCATION}-docker.pkg.dev/${PROJECT_ID}/docker-repo"
export IMAGE_NAME="cookeo-a-retro"
export BRANCH_NAME=$(git branch --show-current)
```

Authentification sur Google Artifact Repositories

```sh
gcloud auth print-access-token \
  --impersonate-service-account ${SERVICE_ACCOUNT} | docker login \
  -u oauth2accesstoken \
  --password-stdin https://${GAR_LOCATION}-docker.pkg.dev
```

Pour contruire l'image docker en local :

```sh
docker build \
  -t ${GAR_REPOSITORY}/${IMAGE_NAME}-${BRANCH_NAME} \
  . \
```

> [!CAUTION]
> Sur les MacBook avec une puce M1, il est nécessaire d'ajouter l'option de build `--platform linux/amd64` à la commande `docker build`
> ```sh
> docker build \
>   -t ${GAR_REPOSITORY}/${IMAGE_NAME} \
>   . \
>   --platform linux/amd64
> ```

Pour tester localement l'image docker :

```sh
docker run -p 5000:5000 ${GAR_REPOSITORY}/${IMAGE_NAME}-${BRANCH_NAME}
```

Pousser l'image sur Google Artifact Repositories :

```sh
docker push ${GAR_REPOSITORY}/${IMAGE_NAME}-${BRANCH_NAME}
```

Déployer manuellement sur Google Cloud Run :

```sh
gcloud run deploy ${IMAGE_NAME} \
  --image ${GAR_REPOSITORY}/${IMAGE_NAME}-${BRANCH_NAME} \
  --region ${GAR_LOCATION} \
  --platform managed \
  --port 5000
```