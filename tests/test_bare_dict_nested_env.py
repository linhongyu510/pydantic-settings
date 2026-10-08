"""Regression tests for bare typing.Dict with env_nested_delimiter.

See https://github.com/pydantic/pydantic-settings/issues/1007
"""

from typing import Dict

from pydantic_settings import BaseSettings, SettingsConfigDict


def test_nested_env_bare_dict_annotation(env):
    """A bare (unparameterized) typing.Dict field should not raise IndexError
    when env_nested_delimiter is set and a nested env var exists."""

    class Settings(BaseSettings):
        top: Dict

        model_config = SettingsConfigDict(env_nested_delimiter='__')

    env.set('TOP__K', 'v')
    cfg = Settings()
    assert cfg.model_dump() == {'top': {'k': 'v'}}


def test_nested_env_bare_dict_inside_model(env):
    """A bare typing.Dict inside a nested model should also work."""
    from pydantic import BaseModel

    class Sub(BaseModel):
        dvals: Dict

    class Settings(BaseSettings):
        sub: Sub

        model_config = SettingsConfigDict(env_nested_delimiter='__')

    env.set('SUB__DVALS__K', 'v')
    cfg = Settings()
    assert cfg.model_dump() == {'sub': {'dvals': {'k': 'v'}}}
