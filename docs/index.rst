.. Grami AI documentation master file

Grami AI: Dynamic AI Agent Framework
=====================================

.. image:: https://img.shields.io/badge/version-0.1.0-blue.svg
   :target: https://github.com/your-username/grami-ai
   :alt: Version

.. image:: https://img.shields.io/badge/python-3.8+-blue.svg
   :target: https://www.python.org/downloads/
   :alt: Python Versions

.. image:: https://img.shields.io/badge/license-MIT-green.svg
   :target: LICENSE
   :alt: License

Welcome to Grami AI's documentation!
------------------------------------

Grami AI is a cutting-edge, flexible framework for creating dynamic and intelligent AI agents. Designed with modern Python async/await paradigms, Grami enables developers to build powerful AI-driven applications with ease.

.. contents:: Table of Contents
   :depth: 3
   :local:

Features
--------

- **Multi-LLM Support**: Compatible with multiple Language Models
- **Dynamic Agent Creation**: Define agents with specific roles and capabilities
- **Streaming Responses**: Token-by-token response generation
- **Extensible Tool Ecosystem**: Easily add custom tools and capabilities
- **Asynchronous Design**: Built for high-performance, non-blocking operations

Quick Start
-----------

Installation
^^^^^^^^^^^^

.. code-block:: bash

   pip install grami-ai

Basic Usage
^^^^^^^^^^^

.. code-block:: python

   from grami.agent import Agent
   from grami.providers import GeminiProvider
   from grami.tools import CalculatorTool

   async def main():
       math_agent = Agent(
           name="MathAssistant",
           role="Mathematical Problem Solver",
           llm_provider=GeminiProvider(api_key="your_api_key"),
           tools=[CalculatorTool()],
           initial_context=[
               {
                   "role": "system", 
                   "content": "You are a helpful math assistant."
               }
           ]
       )

       response = await math_agent.send_message("Calculate the area of a circle with radius 5")
       print(response)

Supported Language Models
------------------------

- Google Gemini
- OpenAI GPT
- Anthropic Claude (Coming Soon)

Documentation Sections
---------------------

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   installation
   getting_started
   agents
   providers
   tools
   examples
   contributing
   license

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
