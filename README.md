
## setup

### local key

create local age key

``` bash
age-keygen -o key.txt
```

export sops environment variable for the age key

``` bash
export SOPS_AGE_KEY_FILE=key.txt
```

### gcp kms

activate kms api

``` bash
gcloud services enable cloudkms.googleapis.com
```

create key ring

``` bash
gcloud kms keyrings create cursor-keyring --location global
```

create encryption key for sops

``` bash
gcloud kms keys create cursor-key --location=global --keyring=cursor-keyring --purpose=encryption
```

list keys

``` bash
gcloud kms keys list --keyring=cursor-keyring --location=global
```

## encryption rules

`.sops.yaml` is used to configure sops to use both the local age key and the gcp kms key for encryption

``` bash
creation_rules:
  - path_regex: \.(secrets|creds)\.yml$
    gcp_kms: projects/xxx/locations/global/keyRings/xxx/cryptoKeys/cursor-key
    age: age1xxx
```

currently:
- `.creds.yml` is encrypted with the gcp kms key and 
- `.secrets.yml` is encrypted with the gcp kms key

## tests after removing the key from gcp kms

`.creds.yml` is still able to be decrypted with the local key

``` bash
sops -d .creds.yml  # succeeds
sops -d --age "$(cat key.txt)" .creds.yml  # succeeds
```

`.secrets.yml` is no longer able to be decrypted because it requires the gcp kms key

``` bash
sops -d .secrets.yml  # fails
sops -d --gcp-kms cursor-keyring/global/cursor-key .secrets.yml  # fails
```

## usage

encrypt secrets

``` bash
sops -e .secrets.yml
```

edit secrets

``` bash
sops .secrets.yml
```
