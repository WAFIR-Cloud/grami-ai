# grami-ai

Open-source Python library for building AI-powered Instagram marketing tools with Gemini.

**grami-ai** provides a set of tools and abstractions to simplify the development of intelligent Instagram bots and marketing applications. It leverages the power of Google Gemini for advanced AI capabilities and integrates seamlessly with other essential services like Redis and Amazon S3.

## Features

* **Shared Memory Wrapper:** A convenient interface for managing shared state in Redis, enabling efficient communication and data sharing between different components of your application.
* **Event Publisher/Consumer (Coming Soon):**  Asynchronous communication between AI agents using Kafka. (This will be added when you implement `events.py`)
* **Gemini API Wrapper (Coming Soon):**  Simplified interactions with the Gemini API for tasks like content generation, image analysis, and more. (This will be added when you implement `gemini.py`)
* **S3 Wrapper (Coming Soon):**  Easy-to-use functions for media upload, storage, and retrieval with Amazon S3. (This will be added when you implement `s3.py`)

## Installation

```bash
pip install grami-ai
from grami_ai import state

# Set a value
await state.set("my_key", "my_value")

# Get a value
value = await state.get("my_key")

# Delete a key
await state.delete("my_key")

# Check if a key exists
exists = await state.exists("my_key")
```
MIT License

Copyright (c) 2024 WAFIR Cloud LLC

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.