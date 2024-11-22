from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="grami-ai",
    version="0.2.310",
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
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires='>=3.8',
    install_requires=[
        'aiokafka>=0.9.1',
        'aioredis>=2.0.1',
        'asyncio',
        'aiohttp>=3.9.3',
        'beautifulsoup4>=4.12.3',
        'typing-extensions>=4.10.0',
        'pydantic>=2.6.4',
        'pydantic-settings>=2.2.1',
        'fastapi>=0.110.0',
        'uvicorn>=0.27.1',
        'python-jose[cryptography]>=3.3.0',
        'passlib[bcrypt]>=1.7.4',
        'python-multipart>=0.0.9',
        'tenacity>=8.2.3',
        'aiofiles>=23.2.1',
        'jinja2>=3.1.3',
        'pillow>=10.2.0',
        'python-dotenv>=1.0.1',
        'openai>=1.14.3',
        'anthropic>=0.20.0',
        'google-generativeai>=0.4.1',
    ],
    extras_require={
        'storage': {
            'motor>=3.1.1',
            'pymongo>=4.3.3',
            'sqlalchemy>=2.0.0',
            'alembic>=1.11.1',
            'asyncpg>=0.28.0',
        },
        'monitoring': {
            'prometheus-client>=0.17.0',
            'opentelemetry-api>=1.19.0',
            'opentelemetry-sdk>=1.19.0',
            'opentelemetry-instrumentation>=0.40b0',
        },
        'dev': [
            'pytest>=7.3.1',
            'pytest-asyncio>=0.21.0',
            'pytest-cov>=4.1.0',
            'mypy>=1.3.0',
            'black>=23.3.0',
            'flake8>=6.0.0',
            'isort>=5.12.0',
            'pre-commit>=3.3.3',
        ],
        'docs': [
            'sphinx>=4.5.0',
            'sphinx-rtd-theme>=1.0.0',
            'sphinx-autodoc-typehints>=1.18.3',
            'sphinxcontrib-napoleon>=0.7',
            'mkdocs-material>=9.1.18',
            'mkdocstrings[python]>=0.22.0',
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
