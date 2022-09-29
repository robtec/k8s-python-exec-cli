# Run a Python script on a K8s Pod

This is a small project that allows users to copy a script to a pod for execution

## How it works

The `pod_exec.py` copies a given script to a pod for it to be ran on that pod

## Setup

```commandline
$ pip3 install -r requirements.txt
```
## Example

Log into the k8s cluster before running the next command

```commandline
$ python3 pod_exec.py --pod python-pod --pvc task-pv-claim --script say_hello.py

 Hello, It's me, I'm running on host python
```

The above result is from `say_hello.py`, which is copied to the pod and then executed.