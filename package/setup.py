from setuptools import setup, find_packages
from pathlib import Path

# Developer self-reminder for uploading to pypi:
# - cd package
# - install: wheel, twine
# - build  : python setup.py bdist_wheel
# - deploy : twine upload dist/*
# https://kynan.github.io/blog/2020/05/23/how-to-upload-your-package-to-the-python-package-index-pypi-test-server

this_dir = Path(__file__).parent.parent
# long_description = (this_dir / "README.md").read_text(encoding="utf-8")


def parse_requirements(filename):
    with open(filename, "r") as f:
        reqs = [line.strip() for line in f if line.strip() and not line.startswith("#")]
    return reqs

setup(
    name="aicard",
    version="0.3.3",
    packages=find_packages(),
    install_requires=parse_requirements("requirements.txt"),
    description="Compute and organize model cards locally or online.",
    author="CERTH",
    author_email="gnikoul@gmail.com",
    url="https://github.com/mever-team/transparency-service",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Development Status :: 3 - Alpha",
    ],
    python_requires=">=3.11",
    # long_description=long_description,
    long_description_content_type="text/markdown",
)
