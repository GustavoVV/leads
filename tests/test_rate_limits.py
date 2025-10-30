import json

from apps.api.schemas.base import RateLimitConfig


def test_rate_limit_config_parsing():
    raw = "{""default_per_minute"": 25, ""followup_per_day"": 2}"
    parsed = RateLimitConfig.model_validate_json(raw)
    assert parsed.default_per_minute == 25
    assert parsed.followup_per_day == 2
