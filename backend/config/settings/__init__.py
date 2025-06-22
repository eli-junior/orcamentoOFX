from decouple import config

match ENVIRONMENT := (config("ENVIRONMENT")).lower():
    case "production":
        from .production import *  # noqa: F403
    case "development":
        from .development import *  # noqa: F403
    case _:
        raise ValueError(
            f"Unknown environment: {ENVIRONMENT}. Expected 'production' or 'development'."
        )
