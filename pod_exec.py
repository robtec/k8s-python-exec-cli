import argparse
import os
import tarfile
from tempfile import TemporaryFile

from kubernetes import config
from kubernetes.client import Configuration
from kubernetes.client.api import core_v1_api
from kubernetes.client.rest import ApiException
from kubernetes.stream import stream

def check_resources_exist(api_instance, args):

    resp = None

    pod_name = args.pod
    namespace = args.namespace
    pvc_name = args.pvc

    try:
        resp = api_instance.read_namespaced_pod(name=pod_name,
                                                namespace=namespace)
    except ApiException as e:
        if e.status != 404:
            print("Unknown error: %s" % e)
            exit(1)

    if not resp:
        print("Pod %s does not exist in namespace %s, exiting." % (pod_name, namespace))
        exit(1)

    try:
        pvcs = api_instance.list_persistent_volume_claim_for_all_namespaces(watch=False)

        expected_pvc = [pvc for pvc in pvcs.items if pvc.metadata.name == pvc_name]

        if not expected_pvc:
            print("Pvc %s does not exist in namespace %s, exiting." % (pvc_name, namespace))
            exit(1)

    except ApiException as e:
        if e.status != 404:
            print("Unknown error: %s" % e)
            exit(1)

def exec_commands(api_instance, args):

    pod_name = args.pod
    namespace = args.namespace

    check_resources_exist(api_instance, args)

    python_command = "python /tmp/%s" % args.script

    exec_command = [
        args.shell,
        '-c',
        python_command]

    resp = stream(api_instance.connect_get_namespaced_pod_exec,
                  pod_name,
                  namespace,
                  command=exec_command,
                  stderr=True, stdin=False,
                  stdout=True, tty=False)

    print(resp)

def copy_file_to_pod(api_instance, args):

    pod_name = args.pod
    namespace = args.namespace

    check_resources_exist(api_instance, args)

    source_file = args.script
    dest_dir = args.dir

    exec_command = ['tar', 'xvf', '-', '-C', dest_dir]
    resp = stream(api_instance.connect_get_namespaced_pod_exec, pod_name, namespace,
                  command=exec_command,
                  stderr=True, stdin=True,
                  stdout=True, tty=False,
                  _preload_content=False)

    with TemporaryFile() as tar_buffer:
        with tarfile.open(fileobj=tar_buffer, mode='w') as tar:
            tar.add(source_file)

        tar_buffer.seek(0)
        commands = []
        commands.append(tar_buffer.read())

        while resp.is_open():
            resp.update(timeout=1)
            if resp.peek_stdout():
                print("STDOUT: %s" % resp.read_stdout())
            if resp.peek_stderr():
                print("STDERR: %s" % resp.read_stderr())
            if commands:
                c = commands.pop(0)
                resp.write_stdin(c)
            else:
                break
        resp.close()

def main():

    parser = argparse.ArgumentParser(description="Copy file to pod and run it")
    parser.add_argument("--pod", type=str, help="name of pod to exec", required=True)
    parser.add_argument("--namespace", type=str, help="namespace of pod", default="default")
    parser.add_argument("--script", type=str, help="script to copy to pod", required=True)
    parser.add_argument("--dir", type=str, help="dir where to copy script", default="/tmp/")
    parser.add_argument("--shell", type=str, help="remote exec shell", default="/bin/sh")
    parser.add_argument("--pvc", type=str, help="pvc name", required=True)

    args = parser.parse_args()

    if "KUBERNETES_SERVICE_HOST" in os.environ:
        config.load_incluster_config()
    else:
        config.load_kube_config()

    try:
        c = Configuration().get_default_copy()
    except AttributeError:
        c = Configuration()
        c.assert_hostname = False
    Configuration.set_default(c)
    core_v1 = core_v1_api.CoreV1Api()

    copy_file_to_pod(core_v1, args)

    exec_commands(core_v1, args)

if __name__ == '__main__':
    main()