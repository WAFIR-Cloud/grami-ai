from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="grami-ai",
    version="0.2.0",
    author="Grami AI Team",
    author_email="support@grami.ai",
    description="Async AI Agent Framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/grami-ai/framework",
    packages=find_packages(exclude=['tests*', 'Examples*']),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires='>=3.8',
    install_requires=[
        'aiokafka>=0.8.1',
        'aioredis>=2.0.1',
        'asyncio',
        'aiohttp>=3.8.4',
        'beautifulsoup4>=4.12.2',
        'typing-extensions>=4.5.0',
    ],
    extras_require={
        'gemini': ['google-generativeai'],
        'ollama': ['requests'],
        'dev': [
            'pytest>=7.3.1',
            'pytest-asyncio>=0.21.0',
            'mypy>=1.3.0',
            'black',
            'flake8'
        ],
        'docs': [
            'sphinx>=4.5.0',
            'sphinx-rtd-theme>=1.0.0',
            'sphinx-autodoc-typehints>=1.18.3',
            'sphinxcontrib-napoleon>=0.7'
        ]
    },
    keywords=[
        'ai', 
        'agent', 
        'llm', 
        'language-model', 
        'generative-ai', 
        'chatbot', 
        'machine-learning',
        'async',
        'tools'
    ],
    project_urls={
        'Documentation': 'https://grami-ai.readthedocs.io/',
        'Source': 'https://github.com/grami-ai/framework',
        'Tracker': 'https://github.com/grami-ai/framework/issues',
    },
)
