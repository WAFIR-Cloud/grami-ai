from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="grami-ai",
    version="0.3.0",
    author="Grami AI Team",
    author_email="support@grami.ai",
    description="Flexible Multi-Agent AI Framework with Advanced WebSocket Communication",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/grami-ai/framework",
    packages=find_packages(exclude=['tests*', 'examples*', 'docs*']),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Framework :: AsyncIO",
    ],
    keywords=[
        "ai", 
        "async", 
        "websocket", 
        "multi-agent", 
        "content-generation", 
        "machine-learning"
    ],
    python_requires='>=3.9',
    install_requires=[
        # Core Async and Web Libraries
        'asyncio',
        'aiohttp>=3.9.3',
        'websockets>=12.0',
        'fastapi>=0.110.0',
        'uvicorn>=0.27.1',

        # Configuration and Environment
        'python-dotenv>=1.0.1',
        'pydantic>=2.6.4',
        'pydantic-settings>=2.2.1',

        # Data Processing and Utilities
        'typing-extensions>=4.10.0',
        'tenacity>=8.2.3',
        'aiofiles>=23.2.1',
        'pillow>=10.2.0',
        'beautifulsoup4>=4.12.3',

        # Authentication and Security
        'python-jose[cryptography]>=3.3.0',
        'passlib[bcrypt]>=1.7.4',
        'python-multipart>=0.0.9',

        # Templating and Rendering
        'jinja2>=3.1.3',

        # LLM and AI Providers
        'openai>=1.14.3',
        'anthropic>=0.20.0',
        'google-generativeai>=0.4.1',

        # Optional but Recommended
        'redis>=5.0.3',  # For backend memory management
    ],
    extras_require={
        'dev': [
            'pytest>=7.4.4',
            'pytest-asyncio>=0.23.3',
            'mypy>=1.9.0',
            'ruff>=0.3.3',
            'black>=24.3.0',
        ],
        'docs': [
            'mkdocs>=1.5.3',
            'mkdocstrings[python]>=0.24.0',
        ],
    },
    entry_points={
        'console_scripts': [
            'grami-ai=grami_ai.cli:main',
        ],
    },
    project_urls={
        'Documentation': 'https://github.com/grami-ai/framework/docs',
        'Source': 'https://github.com/grami-ai/framework',
        'Tracker': 'https://github.com/grami-ai/framework/issues',
    },
    include_package_data=True,
    zip_safe=False
)
