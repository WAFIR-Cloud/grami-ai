Testing Guide
=============

This guide covers testing practices and tools used in the GRAMI AI framework.

Test Infrastructure
-----------------

GRAMI AI uses pytest as its primary testing framework, with several plugins and tools to ensure code quality:

* ``pytest``: Core testing framework
* ``pytest-asyncio``: Async test support
* ``pytest-cov``: Coverage reporting
* ``pytest-mock``: Mocking utilities
* ``pytest-timeout``: Test timeouts
* ``pytest-xdist``: Parallel test execution

Running Tests
------------

The project includes a Makefile with several testing commands:

.. code-block:: bash

    # Run full test suite with coverage
    make test

    # Run fast tests (excludes slow/integration tests)
    make test-fast

    # Run tests in watch mode
    make test-watch

    # Run all checks (format, lint, test)
    make check

Test Organization
---------------

Tests are organized in the ``tests/`` directory:

* ``test_agent.py``: Agent functionality tests
* ``test_config.py``: Configuration system tests
* ``test_core.py``: Core utilities tests
* ``test_events.py``: Event system tests
* ``test_memory.py``: Memory backend tests
* ``test_tools.py``: Tool system tests

Test Categories
-------------

Tests are categorized using pytest markers:

* ``@pytest.mark.slow``: Time-intensive tests
* ``@pytest.mark.integration``: Tests requiring external services
* ``@pytest.mark.requires_redis``: Tests requiring Redis
* ``@pytest.mark.requires_postgres``: Tests requiring PostgreSQL
* ``@pytest.mark.requires_network``: Tests requiring network access

To run specific test categories:

.. code-block:: bash

    # Run only fast tests
    pytest -m "not slow"

    # Run only unit tests (no integration)
    pytest -m "not integration"

Test Configuration
----------------

Test settings are configured in ``pytest.ini``:

* Async test support
* Test discovery patterns
* Output formatting
* Coverage reporting
* Custom markers

Development Setup
---------------

1. Install test dependencies:

   .. code-block:: bash

       pip install -r requirements-test.txt

2. Install pre-commit hooks:

   .. code-block:: bash

       make dev-setup

Code Quality Tools
----------------

The framework uses several tools to maintain code quality:

* ``black``: Code formatting
* ``isort``: Import sorting
* ``flake8``: Style guide enforcement
* ``pylint``: Code analysis
* ``mypy``: Type checking
* ``bandit``: Security scanning
* ``safety``: Dependency security checks

Run all quality checks:

.. code-block:: bash

    make lint

Writing Tests
-----------

Follow these guidelines when writing tests:

1. Use appropriate fixtures from ``conftest.py``
2. Mock external dependencies
3. Use type hints
4. Include docstrings
5. Follow the Arrange-Act-Assert pattern

Example test:

.. code-block:: python

    @pytest.mark.asyncio
    async def test_memory_operations(redis_memory):
        """Test basic memory operations."""
        # Arrange
        conversation_id = "test_conv"
        test_data = {"key": "value"}

        # Act
        await redis_memory.add_item(conversation_id, test_data)
        result = await redis_memory.get_items(conversation_id)

        # Assert
        assert len(result) == 1
        assert result[0] == test_data

Coverage Requirements
------------------

* Minimum coverage: 80%
* Coverage reports: HTML and terminal
* Uncovered lines are highlighted

View coverage report:

.. code-block:: bash

    # Run tests with coverage
    make test

    # Open HTML coverage report
    open htmlcov/index.html

Continuous Integration
-------------------

The test suite runs in CI for:

* Pull requests
* Main branch commits
* Release tags

CI runs:

1. Linting and type checks
2. Unit tests
3. Integration tests
4. Security scans
5. Coverage reporting

Contributing Tests
----------------

When contributing new features:

1. Add corresponding tests
2. Update existing tests if needed
3. Ensure all tests pass
4. Maintain or improve coverage
5. Add any new test dependencies to ``requirements-test.txt``
