from decouple import config

match ENVIROMENT := (config("ENVIROMENT", default="development")).lower():
    case "production":
        from .production import *  # noqa: F403
    case "development":
        from .development import *  # noqa: F403
    case _:
        raise ValueError(
            f"Unknown environment: {ENVIROMENT}. Expected 'production' or 'development'."
        )
