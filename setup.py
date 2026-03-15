from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="open-anamnesis",
    version="0.1.0",
    author="Your Name",
    description="A dbt-like platform for building and managing flashcard projects",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/open-anamnesis",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "click>=8.0.0",
        "pyyaml>=5.4.0",
        "jsonschema>=4.0.0",
        "jinja2>=3.0.0",
        "flask>=2.0.0",
    ],
    entry_points={
        "console_scripts": [
            "anamnesis=open_anamnesis.cli:main",
            "anamnesis-compile=open_anamnesis.cli:compile_cmd",
            "anamnesis-build=open_anamnesis.cli:build_cmd",
        ],
    },
)
