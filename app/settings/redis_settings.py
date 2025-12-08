from pydantic import SecretStr

from app.settings.base import BaseConfig


class RedisSettings(BaseConfig):
    REDIS_PASSWORD: SecretStr = SecretStr('default_pwd')
    REDIS_PORT: str = "6379"
    REDIS_HOST: str = "db_redis"

    @property
    def redis_dsn(self) -> str:
        password = self.REDIS_PASSWORD.get_secret_value()
        return f"redis://:{password}@{self.REDIS_HOST}:{self.REDIS_PORT}/0"


redis_settings = RedisSettings()
print(redis_settings.redis_dsn)
