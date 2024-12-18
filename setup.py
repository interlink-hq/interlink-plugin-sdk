from typing import List
import setuptools


def get_version() -> str:
    with open("version.txt", encoding="utf-8") as fh:
        return fh.read()


def get_readme() -> str:
    with open("README.md", encoding="utf-8") as fh:
        return fh.read()


def get_requirements(filename: str) -> List[str]:
    req_list = []
    with open(filename, encoding="utf-8") as f:
        for line in f.readlines():
            req = line.strip()
            if not req or req.startswith(("-e", "#")):
                continue
            req_list.append(req)
    return req_list


if __name__ == "__main__":
    setuptools.setup(
        name="interlink",
        version=get_version(),
        author="Mauro Gattari",
        author_email="mauro.gattari@infn.it",
        description="InterLink Plugin SDK",
        long_description=get_readme(),
        long_description_content_type="text/markdown",
        url="package URL",
        project_urls={},
        classifiers=[
            "Programming Language :: Python :: 3",
            "Operating System :: OS Independent",
        ],
        packages=["interlink"],
        python_requires=">=3.11",
        install_requires=get_requirements("requirements.txt"),
        extras_require={"dev": get_requirements("requirements-dev.txt")},
    )
