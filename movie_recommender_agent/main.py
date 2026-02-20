# |---------------------------------------------------------|
# |                                                         |
# |                 Give Feedback / Get Help                |
# | https://github.com/getbindu/Bindu/issues/new/choose    |
# |                                                         |
# |---------------------------------------------------------|
#
#  Thank you users! We ❤️ you! - 🌻

"""Movie Recommender Agent - Intelligent film recommendation system.

Provides personalized movie suggestions based on preferences, ratings, and trends.
Uses Exa search for up-to-date movie information, ratings, and reviews.
"""

import argparse
import asyncio
import json
import os
import sys
import traceback
from pathlib import Path
from textwrap import dedent
from typing import Any

from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from agno.tools.exa import ExaTools
from agno.tools.mem0 import Mem0Tools
from bindu.penguin.bindufy import bindufy
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Global instances
agent: Agent | None = None
_initialized = False
_init_lock = asyncio.Lock()


class APIKeyError(ValueError):
    """API key is missing."""


def load_config() -> dict:
    """Load agent configuration from project root."""
    possible_paths = [
        Path(__file__).parent.parent / "agent_config.json",  # Project root
        Path(__file__).parent / "agent_config.json",  # Same directory
        Path.cwd() / "agent_config.json",  # Current working directory
    ]

    for config_path in possible_paths:
        if config_path.exists():
            try:
                with open(config_path) as f:
                    return json.load(f)
            except Exception as e:
                print(f"⚠️  Error reading {config_path}: {e}")
                continue

    # Default configuration
    return {
        "name": "movie-recommender-agent",
        "description": "AI-powered movie recommendation system with personalized suggestions",
        "version": "1.0.0",
        "deployment": {
            "url": "http://127.0.0.1:3773",
            "expose": True,
            "protocol_version": "1.0.0",
            "proxy_urls": ["127.0.0.1"],
            "cors_origins": ["*"],
        },
        "environment_variables": [
            {
                "key": "OPENROUTER_API_KEY",
                "description": "OpenRouter API key for LLM calls (required)",
                "required": True,
            },
            {
                "key": "MODEL_NAME",
                "description": "Model ID for OpenRouter",
                "required": False,
            },
            {
                "key": "EXA_API_KEY",
                "description": "Exa API key for movie information search (required)",
                "required": True,
            },
            {
                "key": "MEM0_API_KEY",
                "description": "Mem0 API key for memory operations",
                "required": False,
            },
        ],
    }


def _get_api_keys() -> tuple[str | None, str | None, str | None, str]:
    """Get API keys and configuration from environment."""
    openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
    mem0_api_key = os.getenv("MEM0_API_KEY")
    exa_api_key = os.getenv("EXA_API_KEY")
    model_name = os.getenv("MODEL_NAME", "openai/gpt-4o")
    return openrouter_api_key, mem0_api_key, exa_api_key, model_name


def _create_llm_model(openrouter_api_key: str, model_name: str) -> OpenRouter:
    """Create and return the OpenRouter model."""
    if not openrouter_api_key:
        error_msg = (
            "OpenRouter API key is required. Set OPENROUTER_API_KEY environment variable.\n"
            "Get an API key from: https://openrouter.ai/keys"
        )
        raise APIKeyError(error_msg)

    return OpenRouter(
        id=model_name,
        api_key=openrouter_api_key,
        cache_response=True,
        supports_native_structured_outputs=True,
    )


def _setup_tools(mem0_api_key: str | None, exa_api_key: str) -> list:
    """Set up all tools for the movie recommender agent."""
    tools = []

    # ExaTools is required for movie information search
    try:
        exa_tools = ExaTools(api_key=exa_api_key)
        tools.append(exa_tools)
        print("🎬 Exa search enabled for movie information and ratings")
    except Exception as e:
        print(f"❌ Failed to initialize ExaTools: {e}")
        raise

    # Optional: Mem0 for conversation memory
    if mem0_api_key:
        try:
            mem0_tools = Mem0Tools(api_key=mem0_api_key)
            tools.append(mem0_tools)
            print("🧠 Mem0 memory system enabled for conversation context")
        except Exception as e:
            print(f"⚠️  Mem0 initialization issue: {e}")

    return tools


async def initialize_agent() -> None:
    """Initialize the movie recommender agent."""
    global agent

    openrouter_api_key, mem0_api_key, exa_api_key, model_name = _get_api_keys()

    # Validate required API keys
    if not openrouter_api_key:
        error_msg = (
            "OpenRouter API key is required. Set OPENROUTER_API_KEY environment variable.\n"
            "Get an API key from: https://openrouter.ai/keys"
        )
        raise APIKeyError(error_msg)

    if not exa_api_key:
        error_msg = (
            "Exa API key is required for movie information. Set EXA_API_KEY environment variable.\n"
            "Get an API key from: https://exa.ai"
        )
        raise APIKeyError(error_msg)

    model = _create_llm_model(openrouter_api_key, model_name)
    tools = _setup_tools(mem0_api_key, exa_api_key)

    # Create the movie recommender agent
    agent = Agent(
        name="PopcornPal - Movie Recommender",
        model=model,
        tools=tools,
        description=dedent("""\
            You are PopcornPal, a passionate and knowledgeable film curator with expertise in cinema worldwide! 🎥

            Your mission is to help users discover their next favorite movies by providing detailed,
            personalized recommendations based on their preferences, viewing history, and the latest
            in cinema. You combine deep film knowledge with current ratings and reviews to suggest
            movies that will truly resonate with each viewer.

            Expertise Areas:
            - Global cinema from Hollywood to international films
            - All genres: drama, comedy, thriller, horror, sci-fi, romance, documentary
            - Film history and influential directors
            - Current box office trends and upcoming releases
            - Streaming platform availability
            - Film festivals and award-winning cinema
        """),
        instructions=dedent("""\
            RECOMMENDATION PROCESS:

            1. ANALYSIS PHASE 🎯
               - Carefully analyze user preferences, favorite movies, and specific requests
               - Identify key themes, genres, styles, and mood preferences
               - Consider rating preferences (IMDB, Rotten Tomatoes, etc.)
               - Note any constraints: language, decade, runtime, content ratings

            2. SEARCH & RESEARCH 🔍
               - Use Exa search to find current, accurate movie information
               - Search for: movie details, ratings, reviews, cast information
               - Look for similar movies based on themes, directors, or actors
               - Check for streaming availability when relevant
               - Include upcoming releases for forward-looking recommendations

            3. RECOMMENDATION CRITERIA 🏆
               - Focus on highly-rated films (IMDB 7.5+, Rotten Tomatoes 80%+ when possible)
               - Include a mix of popular and hidden gem recommendations
               - Consider diverse genres unless specifically requested
               - Balance between classic films and recent releases
               - Include international cinema when appropriate

            4. RESPONSE STRUCTURE 📋
               For each movie recommendation, include:
               - 🎬 Title and release year
               - ⭐ Rating (IMDB/Rotten Tomatoes)
               - 🎭 Genre(s) and subgenres
               - ⏱️ Runtime
               - 🎞️ Director and key cast members
               - 📝 Brief, engaging plot summary (no spoilers)
               - 🎟️ Content rating (PG, R, etc.)
               - 🌐 Language and country of origin
               - 💡 Why it matches the user's preferences

            5. FORMATTING REQUIREMENTS ✨
               - Use clear markdown formatting with emojis
               - Present main recommendations in a structured table
               - Group similar movies together thematically
               - Include 5-10 recommendations per query
               - Add "Bonus Recommendations" section for additional options
               - Mention if movies are available on popular streaming platforms

            6. SPECIAL SCENARIOS 🎪
               - For "I don't know what to watch": Suggest genre samplers
               - For mood-based requests: Match films to emotional tone
               - For group watching: Consider diverse audience appeal
               - For educational purposes: Include films with cultural/historical significance
               - For date nights: Suggest appropriate romantic/engaging films

            7. QUALITY STANDARDS ✅
               - Verify all movie information is current and accurate
               - Never recommend movies you haven't researched
               - Acknowledge when information is limited or uncertain
               - Provide alternatives when exact matches aren't available
               - Always explain your reasoning for each recommendation
        """),
        expected_output=dedent("""\
            # 🎬 Movie Recommendations for [User Request]

            ## 🎯 Based on your preferences for: [Key preferences summary]

            ### 🏆 Top Recommendations

            | Movie | Year | Rating | Genre | Runtime | Why You Might Like It |
            |-------|------|--------|-------|---------|----------------------|
            | **[Movie 1]** | 2023 | ⭐ 8.2/10 IMDB | 🎭 Drama, ❤️ Romance | 2h 15m | [Brief explanation of match] |
            | **[Movie 2]** | 2019 | ⭐ 7.9/10 IMDB | 🎬 Thriller, 🔍 Mystery | 1h 58m | [Brief explanation of match] |
            | **[Movie 3]** | 2020 | 🍅 92% RT | 🤣 Comedy, 🎭 Drama | 1h 45m | [Brief explanation of match] |

            ## 🎞️ Detailed Recommendations

            ### 1. **[Movie Title]** (Year)
            **⭐ Rating**: [IMDB/Rotten Tomatoes score]
            **🎭 Genre**: [Primary genres with emojis]
            **⏱️ Runtime**: [Duration]
            **🎞️ Director**: [Director name]
            **🌟 Starring**: [Key actors]
            **🎟️ Rating**: [Content rating]
            **🌐 Language**: [Language], [Country]

            **📖 Synopsis**:
            [Engaging, spoiler-free plot summary]

            **💡 Why this matches your request**:
            [Detailed explanation connecting to user preferences]

            [Repeat for other top recommendations]

            ## 🎪 Bonus Recommendations
            - **[Bonus Movie 1]** - [Brief reason]
            - **[Bonus Movie 2]** - [Brief reason]
            - **[Bonus Movie 3]** - [Brief reason]

            ## 🔮 Upcoming Releases to Watch For
            - **[Upcoming Movie 1]** (Release Date) - [Why it's promising]
            - **[Upcoming Movie 2]** (Release Date) - [Why it's promising]

            ## 💡 Tips for Your Movie Night
            - Consider [viewing suggestion]
            - Pair with [food/drink suggestion] for better experience
            - Watch in [ideal viewing conditions]

            ---
            *Recommendations curated by PopcornPal 🎥*
            *Last updated: {current_date}*
            *Note: Streaming availability may vary by region*
        """),
        add_datetime_to_context=True,
        markdown=True,
    )
    print(f"✅ Movie Recommender agent initialized using {model_name}")
    print("🎬 Exa search enabled for movie information and ratings")
    if mem0_api_key:
        print("🧠 Memory system enabled for conversation context")


async def run_agent(messages: list[dict[str, str]]) -> Any:
    """Run the agent with the given messages."""
    global agent

    if not agent:
        error_msg = "Agent not initialized"
        raise RuntimeError(error_msg)

    return await agent.arun(messages)  # type: ignore[invalid-await]


async def handler(messages: list[dict[str, str]]) -> Any:
    """Handle incoming agent messages with lazy initialization."""
    global _initialized

    async with _init_lock:
        if not _initialized:
            print("🔧 Initializing Movie Recommender Agent...")
            await initialize_agent()
            _initialized = True

    return await run_agent(messages)


async def cleanup() -> None:
    """Clean up any resources."""
    print("🧹 Cleaning up Movie Recommender Agent resources...")


def _setup_environment_variables(args: argparse.Namespace) -> None:
    """Set environment variables from command line arguments."""
    if args.openrouter_api_key:
        os.environ["OPENROUTER_API_KEY"] = args.openrouter_api_key
    if args.mem0_api_key:
        os.environ["MEM0_API_KEY"] = args.mem0_api_key
    if args.exa_api_key:
        os.environ["EXA_API_KEY"] = args.exa_api_key
    if args.model:
        os.environ["MODEL_NAME"] = args.model


def _display_configuration_info() -> None:
    """Display configuration information to the user."""
    print("=" * 60)
    print("🎬 MOVIE RECOMMENDER AGENT")
    print("=" * 60)
    print("📽️ Purpose: Personalized movie recommendations")
    print("🔍 Powered by: Exa search for current movie data")

    config_info = []
    if os.getenv("OPENROUTER_API_KEY"):
        model = os.getenv("MODEL_NAME", "openai/gpt-4o")
        config_info.append(f"🤖 Model: {model}")
    if os.getenv("EXA_API_KEY"):
        config_info.append("🎬 Exa: Movie information and ratings")
    if os.getenv("MEM0_API_KEY"):
        config_info.append("🧠 Memory: Conversation context enabled")

    for info in config_info:
        print(info)

    print("=" * 60)
    print("Example queries:")
    print("• 'Suggest thriller movies similar to Inception'")
    print("• 'Top-rated comedy movies from last 2 years'")
    print("• 'Korean movies similar to Parasite and Oldboy'")
    print("• 'Family-friendly adventure movies with good ratings'")
    print("=" * 60)


def main() -> None:
    """Run the main entry point for the Movie Recommender Agent."""
    parser = argparse.ArgumentParser(description="Movie Recommender Agent - Intelligent film recommendation system")
    parser.add_argument(
        "--openrouter-api-key",
        type=str,
        default=os.getenv("OPENROUTER_API_KEY"),
        help="OpenRouter API key (env: OPENROUTER_API_KEY)",
    )
    parser.add_argument(
        "--mem0-api-key",
        type=str,
        default=os.getenv("MEM0_API_KEY"),
        help="Mem0 API key for conversation memory (optional)",
    )
    parser.add_argument(
        "--exa-api-key",
        type=str,
        default=os.getenv("EXA_API_KEY"),
        help="Exa API key for movie information search (required)",
    )
    parser.add_argument(
        "--model",
        type=str,
        default=os.getenv("MODEL_NAME", "openai/gpt-4o"),
        help="Model ID for OpenRouter (env: MODEL_NAME)",
    )
    args = parser.parse_args()

    _setup_environment_variables(args)
    _display_configuration_info()

    config = load_config()

    try:
        print("\n🚀 Starting Movie Recommender Agent server...")
        print(f"🌐 Access at: {config.get('deployment', {}).get('url', 'http://127.0.0.1:3773')}")
        bindufy(config, handler)
    except KeyboardInterrupt:
        print("\n🛑 Movie Recommender Agent stopped")
    except Exception as e:
        print(f"❌ Error starting agent: {e}")
        traceback.print_exc()
        sys.exit(1)
    finally:
        asyncio.run(cleanup())


if __name__ == "__main__":
    main()
