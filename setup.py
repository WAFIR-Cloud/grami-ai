from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="grami-ai",
    version="0.1.0",
    author="Feras Alawadi",
    author_email="feras@wafircloud.com",
    description="A flexible, LLM-agnostic AI agent framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/grami-ai",
    packages=find_packages(exclude=['tests*', 'Examples*']),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
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
        'asyncio',
    ],
    extras_require={
        'gemini': ['google-generativeai'],
        'ollama': ['requests'],
        'dev': [
            'pytest',
            'pytest-asyncio',
            'mypy',
            'black',
            'flake8'
        ]
    },
    keywords=[
        'ai', 
        'agent', 
        'llm', 
        'language-model', 
        'generative-ai', 
        'chatbot', 
        'machine-learning'
    ],
    project_urls={
        'Documentation': 'https://github.com/yourusername/grami-ai/blob/main/README.md',
        'Source': 'https://github.com/yourusername/grami-ai',
        'Tracker': 'https://github.com/yourusername/grami-ai/issues',
    },
)
