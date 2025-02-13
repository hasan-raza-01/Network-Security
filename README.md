# Network-Security


### Workflows

1. Update config.yaml
2. Update .env[optional]
3. Update the constants
4. Update the entity
5. Update the configuration
6. Update the components
7. Update the pipeline 
8. Update the main.py
9. Update the dvc.yaml

# Setup github secrets:
1. AWS_ACCESS_KEY_ID
2. AWS_SECRET_ACCESS_KEY
3. AWS_REGION
4. AWS_ECR_LOGIN_URI
5. ECR_REPOSITORY_NAME


# Amazon linux 2023
#### check version
```
cat /etc/os-release
```
## Docker Setup In EC2 commands to be Executed
### optinal

```
sudo dnf update -y
```
```
sudo dnf upgrade
```

### required

```
sudo dnf install docker -y
```
```
sudo systemctl start docker
```
```
sudo systemctl enable docker
```
```
sudo usermod -aG docker ec2-user
```
```
newgrp docker
```

### solution: "shasum: command not found"
```
sudo dnf install perl-Digest-SHA -y
```

### solution: "libicu's dependencies not found"
```
sudo dnf install -y libicu
```

### solution: "missing Dotnet Core 6.0 dependencies"
```
sudo dnf install -y dotnet-sdk-6.0
```

