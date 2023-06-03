import time

from kubernetes import client, config
from kubernetes.stream import stream


config.load_kube_config()


class KTestClient:
    def __init__(
        self,
        k_client: client.ApiClient,
        namespace: str,
        poll_timeout_s: int,
    ) -> None:
        self.k_client = k_client
        self.namespace = namespace
        self.poll_timeout_s = poll_timeout_s

    def run_test_job(self, body: client.V1Job) -> None:
        with client.ApiClient() as api_client:
            batch_api = client.BatchV1Api(api_client)
            core_api = client.CoreV1Api(api_client)
            job = batch_api.create_namespaced_job(
                body=body, namespace=self.namespace, pretty=True
            )
            print(f"Job {job.metadata.name} is created")
            pod = self.get_job_pod(core_api, job.metadata.name)
            print(f"Job pod {pod.metadata.name} is created")
            self.wait_for_main_to_start(core_api, pod)
            print("Main container started, start streaming logs...")
            for line in core_api.read_namespaced_pod_log(
                name=pod.metadata.name,
                namespace=self.namespace,
                container="main",
                follow=True,
                _preload_content=False,
            ).stream():
                print(line.decode("utf-8"), end="")

            for container in pod.spec.containers:
                if container.name == "main":
                    continue
                shutdown_script = job.metadata.annotations[
                    f"ktest/shutdown-{container.name}"
                ]
                print(
                    f"Shutting down {container.name} container "
                    f"with script: {shutdown_script}"
                )
                resp = stream(
                    core_api.connect_post_namespaced_pod_exec,
                    name=pod.metadata.name,
                    namespace=self.namespace,
                    container=container.name,
                    command=["sh", "-c", shutdown_script],
                    stderr=True,
                    stdout=True,
                    stdin=False,
                    tty=False,
                )
                print(f"{container.name}: ", resp)

    def wait_for_main_to_start(
        self, core_api: client.CoreV1Api, pod: client.V1Pod
    ) -> None:
        while True:
            pod = core_api.read_namespaced_pod_status(
                name=pod.metadata.name, namespace=self.namespace
            )
            for c in pod.status.container_statuses:
                if c.name == "main" and c.started:
                    return
            print("Wait for main container to start...")
            time.sleep(self.poll_timeout_s)

    def get_job_pod(
        self, core_api: client.CoreV1Api, job_name: str
    ) -> client.V1Pod:
        while True:
            response = core_api.list_namespaced_pod(
                label_selector=f"job-name={job_name}",
                namespace=self.namespace,
            )
            if len(response.items) > 0:
                return response.items[0]
            print("Waiting for job pod to create...")
            time.sleep(self.poll_timeout_s)
