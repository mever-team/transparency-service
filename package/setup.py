from setuptools import setup, find_packages


def parse_requirements(filename):
    with open(filename, "r") as f:
        reqs = [line.strip() for line in f if line.strip() and not line.startswith("#")]
    return reqs


setup(
    name="modelcard",
    version="0.3",
    packages=find_packages(),
    install_requires=parse_requirements("requirements.txt"),
    description="Compute and organize model cards either locally or through an online service.",
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
)
