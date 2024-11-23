Installation
============

This guide will help you install Grami AI and set up your development environment.

Prerequisites
-------------

- Python 3.8+
- pip package manager

Installation Methods
-------------------

Using pip
^^^^^^^^^

.. code-block:: bash

   # Install the latest stable version
   pip install grami-ai

   # Install from GitHub (latest development version)
   pip install git+https://github.com/your-username/grami-ai.git

Virtual Environment (Recommended)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   # Create a virtual environment
   python3 -m venv grami-env

   # Activate the virtual environment
   source grami-env/bin/activate  # On Unix/macOS
   grami-env\Scripts\activate     # On Windows

   # Install Grami AI
   pip install grami-ai

Verifying Installation
---------------------

.. code-block:: python

   import grami
   print(grami.__version__)

Troubleshooting
---------------

- Ensure you have the latest version of pip
- Check your Python version (3.8+ required)
- Verify internet connection during installation
