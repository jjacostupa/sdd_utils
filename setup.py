import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sdd_utils-jjacostupa", # Replace with your own username
    version="0.1",
    author="Juan Acostupa",
    author_email="jjacostupa@gmail.com",
    description="Small utilities for SDD project",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jjacostupa/sdd_utils",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)