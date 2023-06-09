import os
from pathlib import Path

from setuptools import setup  # type: ignore [import]


setup(
    name="kube-tests",
    version=os.environ["GITHUB_REF_NAME"],
    description="Kubernetes test client",
    author="Vladimir Vojtenko",
    author_email="vladimirdev635@gmail.com",
    license="MIT",
    packages=["kube_tests", "kube_tests.loaders", "kube_tests.parsers"],
    package_data={
        "kube_tests": ["py.typed"],
        "kube_tests.loaders": ["py.typed"],
        "kube_tests.parsers": ["py.typed"],
    },
    install_requires=["kubernetes", "pyyaml"],
    long_description=(Path(__file__).parent / "README.md").read_text(),
    long_description_content_type="text/markdown",
)
