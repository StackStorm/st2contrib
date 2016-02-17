# Kubernetes sensor integration

Pack which allows integration with [Kubernetes](https://kubernetes.io/) service.

# Current Status & Capabilities
Creates a StackStorm Sensor (watch) on Kubernetes ThirdPartyResource API endpoint
Listens for new events. If 'ADDED', rule can pick up and create and AWS RDS database.

## Configuration

config.yaml includes:
```yaml
user: ""
password: ""
kubernetes_api_url: "https://kube_api_url"
extension_url: "/apis/extensions/v1beta1/watch/thirdpartyresources"
```
Where kube_api_url = The FQDN to your Kubernetes API endpoint.

Note: Currently SSL verification is turned off. This is a WIP.

## To setup the Kubernetes Pack
```
st2 run packs.setup_virtualenv packs=kubernetes
st2ctl reload
```

Note: AWS pack must be enabled and running


### Kubernetes Specific Settings

The following must be enabled on Kubernetes API in ```kube-apiserver.yaml```

```yaml
--runtime-config=extensions/v1beta1/thirdpartyresources=true,extensions/v1beta1/deployments=true
```

Simply add the line above. kube-api container will automatically restart to accept the change.



### To Test the RDS create event in the Kubernetes Pack

Create a yaml file with something like below:

```yaml
metadata:
  name: mysql-db31.example.com
  labels:
    resource: database
    object: mysql
apiVersion: extensions/v1beta1
kind: ThirdPartyResource
description: "A specification of database for mysql"
versions:
  - name: stable/v1
```

With kubectl run:

```
kubectl create -f name_of_your_file.yaml
```
