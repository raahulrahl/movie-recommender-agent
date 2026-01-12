# |---------------------------------------------------------|
# |                                                         |
# |                 Give Feedback / Get Help                |
# | https://github.com/getbindu/Bindu/issues/new/choose    |
# |                                                         |
# |---------------------------------------------------------|
#
#  Thank you users! We ❤️ you! - 🌻

"""movie-recommender-agent - An Bindu Agent."""

from movie_recommender_agent.__version__ import __version__
from movie_recommender_agent.main import (
    handler,
    initialize_agent,
    main,
    cleanup,
)

__all__ = [
    "__version__",
    "handler",
    "initialize_agent",
    "main",
    "cleanup",
]