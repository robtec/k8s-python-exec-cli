# Run script from ConfigMap

## Build Image

```
$ docker build -t verification-image .
```

## Populate ConfigMap
```
$ kubectl create configmap verification-script --from-file=verification-shell-script.sh
```

## Apply k8s SA, Cluster Role and Bindings
```
$ kubectl apply -f service-account.yaml

$ kubectl apply -f cluster-role.yaml

$ kubectl apply -f cluster-binding.yaml
```

## Create Pod
```
$ kubectl apply -f pod.yaml
```