from datetime import timedelta

from core.envs import envs

DEBUG = envs.debug

SECRET_KEY = envs.secret_key

ACCESS_TOKEN_LIFETIME = timedelta(seconds=envs.jwt_access_token_expire_seconds)

REFRESH_TOKEN_LIFETIME = timedelta(seconds=envs.jwt_refresh_token_expire_seconds)

JWT_ALGORITHM = envs.jwt_algorithm

POSTGRES_URI = f"{envs.postgres_driver}://{envs.postgres_user}:{envs.postgres_password}@\
    {envs.postgres_host}:{envs.postgres_port}/{envs.postgres_db}".replace(" ", "")  # fmt: skip
