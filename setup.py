import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fusio-worker",
    author="Christoph Kappestein",
    author_email="christoph.kappestein@gmail.com",
    description="A Fusio worker implementation to execute Python code.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/apioo/fusio-worker-python",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    python_requires='>=3',
    install_requires=[
        "fastapi >= 0.110",
        "uvicorn[standard] >= 0.29",
        "fusio-worker-runtime >= 0.2.1",
    ]
)
