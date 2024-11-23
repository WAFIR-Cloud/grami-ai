from setuptools import setup, find_packages
import os

# Read the README.md
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Simplified requirements reading
def read_requirements(filename):
    try:
        with open(filename, 'r') as file:
            return [
                line.strip() 
                for line in file 
                if line.strip() and not line.startswith('#') and not line.startswith('-')
            ]
    except FileNotFoundError:
        return []

# Determine package data files
def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join('..', path, filename))
    return paths

setup(
    name="grami-ai",
    version="0.3.106",  # Increment version to ensure uniqueness
    
    # Metadata
    author="YAFATek Solutions",
    author_email="support@yafatek.dev",
    maintainer="YAFATek Solutions",
    maintainer_email="support@yafatek.dev",
    
    # Project Description
    description="Growth and Relationship AI Management Infrastructure",
    long_description=long_description,
    long_description_content_type="text/markdown",
    
    # Project URLs
    url="https://github.com/yafatek/grami-ai",
    project_urls={
        "Bug Tracker": "https://github.com/yafatek/grami-ai/issues",
        "Documentation": "https://github.com/yafatek/grami-ai/blob/main/README.md",
        "Source Code": "https://github.com/yafatek/grami-ai",
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
    install_requires=read_requirements('requirements.txt'),
    
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
