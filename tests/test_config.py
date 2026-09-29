import importlib

import pytest

from app import config


SETTINGS = ['FLASK_RUN_HOST', 'FLASK_RUN_PORT', 'FLASK_DEBUG', 'CORS_ORIGINS']


@pytest.fixture
def load_config(monkeypatch):
    """Reload app.config with only the given environment variables (the .env file is ignored)."""
    def load(**env):
        monkeypatch.setattr('dotenv.load_dotenv', lambda *args, **kwargs: None)
        for name in SETTINGS:
            monkeypatch.delenv(name, raising=False)
        for name, value in env.items():
            monkeypatch.setenv(name, value)
        return importlib.reload(config)

    yield load
    monkeypatch.undo()
    importlib.reload(config)


def test_constants():
    assert config.MONTH == ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']
    assert config.OPTIMAL_SLEEP == 8.5


def test_defaults_without_env(load_config):
    settings = load_config()
    assert settings.HOST == '127.0.0.1'
    assert settings.PORT == 5000
    assert settings.DEBUG is True
    assert settings.CORS_ORIGINS == ['*']


def test_values_from_env(load_config):
    settings = load_config(FLASK_RUN_HOST='0.0.0.0', FLASK_RUN_PORT='8080', FLASK_DEBUG='false')
    assert settings.HOST == '0.0.0.0'
    assert settings.PORT == 8080
    assert settings.DEBUG is False


@pytest.mark.parametrize('value, expected', [
    ('true', True), ('True', True), ('1', True), ('yes', True),
    ('false', False), ('0', False), ('no', False),
])
def test_debug_values(load_config, value, expected):
    assert load_config(FLASK_DEBUG=value).DEBUG is expected


def test_multiple_cors_origins(load_config):
    settings = load_config(CORS_ORIGINS='http://localhost:8000, http://127.0.0.1:8000')
    assert settings.CORS_ORIGINS == ['http://localhost:8000', 'http://127.0.0.1:8000']
