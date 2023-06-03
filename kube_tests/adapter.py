from string import Template
from typing import Any


SCRIPT_TEMPLATE = Template(
    """
    while true; do if $ready_script; then break;
    else echo "Ready script exited with 1, wait 3 seconds";
    sleep 3; fi; done; $main_command
"""
)


class JobAdapter:
    def adapt(self, job: dict[str, Any]) -> dict[str, Any]:
        annotations = job["metadata"].get("annotations", {})
        if "ktest/ready-script" not in annotations:
            raise ValueError("ktest/ready-script annotation is not provided")

        for container in job["spec"]["template"]["spec"]["containers"]:
            if container["name"] == "main":
                main_command = container["command"] + container["args"]
                container["command"] = ["sh", "-c"]
                container["args"] = [
                    SCRIPT_TEMPLATE.substitute(
                        ready_script=annotations["ktest/ready-script"],
                        main_command=" ".join(main_command),
                    )
                ]
                continue
            shutdown_script_key = f"ktest/shutdown-{container['name']}"
            if shutdown_script_key not in annotations:
                raise ValueError(
                    f"{shutdown_script_key} annotation is not provided"
                )

        return job
