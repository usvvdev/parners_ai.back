from enum import StrEnum


class EngineType(StrEnum):
    REDIS = "redis"

    MYSQL = "mysql"

    CLICKHOUSE = "clickhouse"
