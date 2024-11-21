Quickstart
==========

This guide will help you get started with Grami AI quickly.

Basic Usage
----------

1. Create a simple agent:

.. code-block:: python

    from grami_ai.memory import InMemoryAbstractMemory
    from grami_ai.tools import CalculatorTool
    
    # Initialize components
    memory = InMemoryAbstractMemory()
    calculator = CalculatorTool()
    
    # Use the calculator
    result = await calculator.run('add', 5, 3)
    print(result)  # Output: 8

Memory Management
---------------

Store and retrieve conversation history:

.. code-block:: python

    # Store conversation
    await memory.add_item('conv1', {
        'role': 'user',
        'content': 'Hello'
    })
    
    # Retrieve conversation
    items = await memory.get_items('conv1')
    print(items)  # [{'role': 'user', 'content': 'Hello'}]

Web Scraping
-----------

Use the web scraping tool:

.. code-block:: python

    from grami_ai.tools import WebScraperTool
    
    scraper = WebScraperTool()
    content = await scraper.run(
        'https://example.com',
        operation='fetch'
    )
    print(content)

Advanced Usage
------------

Combine multiple tools and memory:

.. code-block:: python

    from grami_ai.tools import (
        CalculatorTool,
        WebScraperTool,
        StringManipulationTool
    )
    
    # Initialize tools
    calculator = CalculatorTool()
    scraper = WebScraperTool()
    string_tool = StringManipulationTool()
    
    # Use tools together
    web_content = await scraper.run(
        'https://example.com/numbers',
        operation='fetch'
    )
    
    cleaned_text = await string_tool.run(
        web_content,
        operation='clean'
    )
    
    numbers = [int(n) for n in cleaned_text.split()]
    result = await calculator.run('add', numbers[0], numbers[1])
    
    # Store result
    await memory.add_item('calculation', {
        'role': 'system',
        'content': f'Result: {result}'
    })
