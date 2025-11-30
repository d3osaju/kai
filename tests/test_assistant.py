"""Tests for assistant functionality."""

import pytest
from kai.core.assistant import Assistant


@pytest.mark.asyncio
async def test_assistant_initialization():
    """Test assistant initialization."""
    assistant = Assistant()
    await assistant.initialize()
    
    assert assistant.config is not None
    assert assistant.plugin_manager is not None


@pytest.mark.asyncio
async def test_assistant_query():
    """Test basic query processing."""
    assistant = Assistant()
    await assistant.initialize()
    
    response = await assistant.async_query("open firefox")
    assert isinstance(response, str)
    assert len(response) > 0
