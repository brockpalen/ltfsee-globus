import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ltfsee-globus",
    version="0.1.0",
    author="Brock Palen",
    author_email="brockp@umich.edu",
    description="API for missing LTFSEE Functions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/brockpalen/ltfsee-globus/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
