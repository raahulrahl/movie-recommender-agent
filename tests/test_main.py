import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from movie_recommender_agent.main import handler, initialize_agent, APIKeyError


@pytest.mark.asyncio
async def test_handler_returns_response():
    """Test that handler accepts messages and returns a response."""
    messages = [{"role": "user", "content": "Hello, how are you?"}]

    # Mock the run_agent function to return a mock response
    mock_response = MagicMock()
    mock_response.run_id = "test-run-id"
    mock_response.status = "COMPLETED"

    # Mock _initialized to skip initialization and run_agent to return our mock
    with (
        patch("movie_recommender_agent.main._initialized", True),
        patch("movie_recommender_agent.main.run_agent", new_callable=AsyncMock, return_value=mock_response),
    ):
        result = await handler(messages)

    # Verify we get a result back
    assert result is not None
    assert result.run_id == "test-run-id"
    assert result.status == "COMPLETED"


@pytest.mark.asyncio
async def test_handler_with_multiple_messages():
    """Test that handler processes multiple messages correctly."""
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What's the weather?"},
    ]

    mock_response = MagicMock()
    mock_response.run_id = "test-run-id-2"

    with (
        patch("movie_recommender_agent.main._initialized", True),
        patch("movie_recommender_agent.main.run_agent", new_callable=AsyncMock, return_value=mock_response) as mock_run,
    ):
        result = await handler(messages)

    # Verify run_agent was called
    mock_run.assert_called_once_with(messages)
    assert result is not None
    assert result.run_id == "test-run-id-2"


@pytest.mark.asyncio
async def test_handler_initialization():
    """Test that handler initializes on first call."""
    messages = [{"role": "user", "content": "Test"}]

    mock_response = MagicMock()
    mock_response.run_id = "test-init-run-id"
    mock_response.status = "COMPLETED"

    # Start with _initialized as False to test initialization path
    with (
        patch("movie_recommender_agent.main._initialized", False),
        patch("movie_recommender_agent.main.initialize_agent", new_callable=AsyncMock) as mock_init,
        patch("movie_recommender_agent.main.run_agent", new_callable=AsyncMock, return_value=mock_response) as mock_run,
        patch("movie_recommender_agent.main._init_lock", new_callable=MagicMock()) as mock_lock,
    ):
        # Configure the lock to work as an async context manager
        mock_lock_instance = MagicMock()
        mock_lock_instance.__aenter__ = AsyncMock(return_value=None)
        mock_lock_instance.__aexit__ = AsyncMock(return_value=None)
        mock_lock.return_value = mock_lock_instance

        result = await handler(messages)

        # Verify initialization was called
        mock_init.assert_called_once()
        # Verify run_agent was called
        mock_run.assert_called_once_with(messages)
        # Verify we got a result
        assert result is not None
        assert result.run_id == "test-init-run-id"
        assert result.status == "COMPLETED"


@pytest.mark.asyncio
async def test_handler_race_condition_prevention():
    """Test that handler prevents race conditions with initialization lock."""
    messages = [{"role": "user", "content": "Test"}]

    mock_response = MagicMock()

    # Test with multiple concurrent calls
    with (
        patch("movie_recommender_agent.main._initialized", False),
        patch("movie_recommender_agent.main.initialize_agent", new_callable=AsyncMock) as mock_init,
        patch("movie_recommender_agent.main.run_agent", new_callable=AsyncMock, return_value=mock_response),
        patch("movie_recommender_agent.main._init_lock", new_callable=MagicMock()) as mock_lock,
    ):
        # Configure the lock to work as an async context manager
        mock_lock_instance = MagicMock()
        mock_lock_instance.__aenter__ = AsyncMock(return_value=None)
        mock_lock_instance.__aexit__ = AsyncMock(return_value=None)
        mock_lock.return_value = mock_lock_instance

        # Call handler twice to ensure lock is used
        await handler(messages)
        await handler(messages)

        # Verify initialize_agent was called only once (due to lock)
        mock_init.assert_called_once()


@pytest.mark.asyncio
async def test_handler_with_movie_query():
    """Test that handler can process a movie recommendation query."""
    messages = [
        {
            "role": "user",
            "content": "Suggest thriller movies similar to Inception",
        }
    ]

    mock_response = MagicMock()
    mock_response.run_id = "movie-run-id"
    mock_response.content = "Movie recommendations generated successfully."

    with (
        patch("movie_recommender_agent.main._initialized", True),
        patch("movie_recommender_agent.main.run_agent", new_callable=AsyncMock, return_value=mock_response),
    ):
        result = await handler(messages)

    assert result is not None
    assert result.run_id == "movie-run-id"
    assert result.content == "Movie recommendations generated successfully."


@pytest.mark.asyncio
async def test_handler_requires_api_key():
    """Test that handler raises error when no API key is provided."""
    messages = [{"role": "user", "content": "Test"}]

    # Configure the lock to work as an async context manager
    mock_lock_instance = MagicMock()
    mock_lock_instance.__aenter__ = AsyncMock(return_value=None)
    mock_lock_instance.__aexit__ = AsyncMock(return_value=None)

    with (
        patch("movie_recommender_agent.main._initialized", False),
        patch("movie_recommender_agent.main.initialize_agent", side_effect=APIKeyError("No API key")),
        patch("movie_recommender_agent.main._init_lock", return_value=mock_lock_instance),
        patch("movie_recommender_agent.main.run_agent", new_callable=AsyncMock),
        pytest.raises(APIKeyError, match="No API key"),
    ):
        await handler(messages)


@pytest.mark.asyncio
async def test_handler_agent_not_initialized():
    """Test that handler raises error when agent is not initialized."""
    messages = [{"role": "user", "content": "Test"}]

    with (
        patch("movie_recommender_agent.main._initialized", True),
        patch("movie_recommender_agent.main.run_agent", side_effect=RuntimeError("Agent not initialized")),
        pytest.raises(RuntimeError, match="Agent not initialized"),
    ):
        await handler(messages)


@pytest.mark.asyncio
async def test_handler_with_exa_api_key_missing():
    """Test that handler raises error when Exa API key is missing."""
    messages = [{"role": "user", "content": "Test"}]

    # Configure the lock to work as an async context manager
    mock_lock_instance = MagicMock()
    mock_lock_instance.__aenter__ = AsyncMock(return_value=None)
    mock_lock_instance.__aexit__ = AsyncMock(return_value=None)

    with (
        patch("movie_recommender_agent.main._initialized", False),
        patch("movie_recommender_agent.main.initialize_agent", side_effect=APIKeyError("Exa API key required")),
        patch("movie_recommender_agent.main._init_lock", return_value=mock_lock_instance),
        patch("movie_recommender_agent.main.run_agent", new_callable=AsyncMock),
        pytest.raises(APIKeyError, match="Exa API key required"),
    ):
        await handler(messages)


@pytest.mark.asyncio
async def test_handler_with_family_movie_query():
    """Test that handler can process a family movie recommendation query."""
    messages = [
        {
            "role": "user",
            "content": "Recommend family-friendly adventure movies for kids aged 8-12",
        }
    ]

    mock_response = MagicMock()
    mock_response.run_id = "family-movie-run-id"
    mock_response.content = "Family movie recommendations generated."

    with (
        patch("movie_recommender_agent.main._initialized", True),
        patch("movie_recommender_agent.main.run_agent", new_callable=AsyncMock, return_value=mock_response),
    ):
        result = await handler(messages)

    assert result is not None
    assert result.run_id == "family-movie-run-id"
    assert result.content == "Family movie recommendations generated."