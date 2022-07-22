# S3 Upload test to Azure Storage Account Containers

## How to upload the python boto3 image to ACR

- Login to ACR
```sh
CONTAINER_REGISTRY_NAME=<container-registry-name>

CONTAINER_REGISTRY_URL="${CONTAINER_REGISTRY_NAME}.azurecr.io"
az acr login --name "${CONTAINER_REGISTRY_NAME}"
```

- Build & Push
```sh
docker build -t "${CONTAINER_REGISTRY_URL}"/tests/s3-upload:1.0.0 docker/.
docker push "${CONTAINER_REGISTRY_URL}"/tests/s3-upload:1.0.0
```

## Create the s3upload job

- Create a namespace for the test (if needed)
```sh
kubectl create ns s3test
```

- Create the configmap with the Azure Storage Account Configurations. <b>Note: validate if config.env has the right values</b>
```sh
k -n s3test create configmap s3test-config --from-env-file=yamls/config.env
```

- Create the secret for the access key:
```sh
AZ_ACCOUNT_ACCESS_SECRET=<copy-secret-here>

k -n s3test create secret generic s3test-credentials --from-literal=AWS_SECRET_ACCESS_KEY="${AZ_ACCOUNT_ACCESS_SECRET}"
```

- Create the s3test job:

> Note: Before applying the yaml, make sure you update to your container registry name in the `yamls/job.yaml` image field.

```sh
kubectl apply -f yamls/job.yaml
```

## Confirm if job completed successfully

```sh
kubectl -n s3test logs s3-upload-xxxxx

AWS_S3_ENDPOINT: http://s3proxy-default.s3proxy-system.svc
AWS_ACCESS_KEY_ID: storageaccountname
AWS_SECRET_ACCESS_KEY: ****
BUCKET_NAME: azure-container-name
Uploading File Name: test-file.txt
Upload Complete.
```
# References

- [Boto3 Python Uploading Files](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-uploading-files.html)
- [Boto3 Python Client Upload File](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.upload_file)
- [Azure Container Registry Docker Push](https://docs.microsoft.com/en-us/azure/container-registry/container-registry-get-started-docker-cli)