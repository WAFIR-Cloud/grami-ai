from setuptools import setup, find_packages
import os

# Read the README.md
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements from requirements.txt
def read_requirements(filename):
    with open(filename, 'r') as file:
        return [line.strip() for line in file if line.strip() and not line.startswith('#')]

# Determine package data files
def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join('..', path, filename))
    return paths

setup(
    name="grami-ai",
    version="0.3.101",
    
    # Metadata
    author="YAFATek Solutions/ GRAMI AI Team",
    author_email="support@yafatek.com",
    maintainer="YAFATek Solutions",
    maintainer_email="supprt@yafatek.com",
    
    # Project Description
    description="Growth and Relationship AI Management Infrastructure",
    long_description=long_description,
    long_description_content_type="text/markdown",
    
    # Project URLs
    url="https://github.com/WAFIR-Cloud/grami-ai",
    project_urls={
        "Bug Tracker": "https://github.com/WAFIR-Cloud/grami-ai/issues",
        "Documentation": "https://github.com/WAFIR-Cloud/grami-ai/blob/main/README.md",
        "Source Code": "https://github.com/WAFIR-Cloud/grami-ai",
    },
    
    # Package Discovery
    packages=find_packages(exclude=['tests*', 'examples*', 'docs*']),
    package_data={
        'grami_ai': package_files('grami_ai'),
    },
    include_package_data=True,
    
    # Classifiers
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet :: WWW/HTTP",
    ],
    
    # Keywords
    keywords=[
        "ai", 
        "agent", 
        "framework", 
        "marketing", 
        "async",
        "generative-ai",
        "llm",
        "machine-learning",
        "artificial-intelligence"
    ],
    
    # Python Version and Dependencies
    python_requires='>=3.10,<3.13',
    
    # Install Requirements
    install_requires=[
        # Core Async and Web Libraries
        'aiohttp>=3.9.3',
        'aioredis>=2.0.1',
        'aiokafka>=0.9.1',
        'fastapi>=0.110.0',
        'uvicorn>=0.27.1',

        # Data Processing and Utilities
        'beautifulsoup4>=4.12.3',
        'typing-extensions>=4.10.0',
        'pydantic>=2.6.0',
        'python-dotenv>=1.0.0',

        # LLM and AI Providers
        'openai>=1.14.3',
        'anthropic>=0.20.0',
        'google-generativeai>=0.4.1',
        'ollama>=0.1.6',

        # Logging and Monitoring
        'structlog>=24.1.0',

        # Optional but Recommended
        'redis>=5.0.1',
    ],
    
    # Optional Dependencies
    extras_require={
        'dev': [
            'pytest>=7.4.4',
            'pytest-asyncio>=0.23.2',
            'mypy>=1.8.0',
            'ruff>=0.2.2',
            'coverage>=7.4.3',
        ],
        'docs': [
            'sphinx>=7.2.6',
            'sphinx-rtd-theme>=2.0.0',
        ],
    },
    
    # Entry Points
    entry_points={
        'console_scripts': [
            'grami-ai=grami_ai.cli:main',
        ],
    },
    
    # Metadata
    zip_safe=False,
    license='MIT',
)
