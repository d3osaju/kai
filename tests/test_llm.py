#!/usr/bin/env python3
"""Test LLM integration."""

import asyncio
from kai.core.assistant import Assistant


async def test_llm():
    """Test LLM integration with Kai."""
    print("Initializing Kai...")
    assistant = Assistant()
    await assistant.initialize()
    
    print("\nTesting general queries with LLM:\n")
    
    queries = [
        "What is Linux?",
        "Tell me a joke",
        "What's 2 + 2?",
    ]
    
    for query in queries:
        print(f"You: {query}")
        response = await assistant.async_query(query)
        print(f"Kai: {response}\n")


if __name__ == "__main__":
    asyncio.run(test_llm())
