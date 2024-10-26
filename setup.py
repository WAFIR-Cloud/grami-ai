from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="grami-ai",
    version="0.1.101",
    author="WAFIR CLOUD",
    author_email="adming@wafir.cloud",
    description="Open-source Python library for building AI-powered Instagram marketing tools with Gemini.",
    # More specific description
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/WAFIR-Cloud/grami-ai",
    packages=find_packages(exclude=["tests"]),  # Exclude the tests directory
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.12",  # Add specific Python versions
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",  # Indicate development status
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    install_requires=[
        "setuptools",
        "pytest",
        "redis",
        "pytest-asyncio",
        "aiokafka",
        " google-generativeai"
    ],
    python_requires=">=3.12",
)
