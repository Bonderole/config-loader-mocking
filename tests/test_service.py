import json
from unittest.mock import patch, mock_open

import pytest

from src.service import ConfigLoader

PATH = "/etc/app/config.json"   # вымышленный путь: реальная ФС в тестах не используется


# ---------- позитивные сценарии ----------
def test_load_success():
    m = mock_open(read_data='{"debug": true}')
    with patch("os.path.exists", return_value=True) as exists, patch("builtins.open", m):
        result = ConfigLoader().load(PATH)

    assert result == {"debug": True}
    exists.assert_called_once_with(PATH)            # путь проверен ровно один раз
    m.assert_called_once_with(PATH, "r")            # файл открыт на чтение с нужным путём
    m().read.assert_called()                        # содержимое действительно прочитано


@pytest.mark.parametrize("content, expected", [
    ('{"debug": true}', {"debug": True}),
    ('{"port": 8080, "host": "localhost"}', {"port": 8080, "host": "localhost"}),
    ('{"nested": {"a": [1, 2, 3]}}', {"nested": {"a": [1, 2, 3]}}),
    ("{}", {}),
])
def test_load_various_valid_contents(content, expected):
    with patch("os.path.exists", return_value=True), patch("builtins.open", mock_open(read_data=content)):
        assert ConfigLoader().load(PATH) == expected


def test_load_non_object_json_is_returned_as_is():
    # фиксируем фактическое поведение: загрузчик не проверяет, что корень – объект
    with patch("os.path.exists", return_value=True), patch("builtins.open", mock_open(read_data="[1, 2]")):
        assert ConfigLoader().load(PATH) == [1, 2]


# ---------- негативные сценарии ----------
def test_file_not_found():
    m = mock_open()
    with patch("os.path.exists", return_value=False) as exists, patch("builtins.open", m):
        with pytest.raises(FileNotFoundError) as err:
            ConfigLoader().load(PATH)

    assert PATH in str(err.value)
    exists.assert_called_once_with(PATH)
    m.assert_not_called()                           # файл даже не пытались открыть


def test_permission_denied():
    m = mock_open()
    m.side_effect = PermissionError(13, "Permission denied")   # недоступные права
    with patch("os.path.exists", return_value=True), patch("builtins.open", m):
        with pytest.raises(PermissionError):
            ConfigLoader().load(PATH)
    m.assert_called_once_with(PATH, "r")


def test_path_is_directory():
    m = mock_open()
    m.side_effect = IsADirectoryError(21, "Is a directory")
    with patch("os.path.exists", return_value=True), patch("builtins.open", m):
        with pytest.raises(IsADirectoryError):
            ConfigLoader().load(PATH)


@pytest.mark.parametrize("content", ["{bad json", "", "not json at all", '{"a": }'])
def test_invalid_json_content(content):
    with patch("os.path.exists", return_value=True), patch("builtins.open", mock_open(read_data=content)):
        with pytest.raises(json.JSONDecodeError):
            ConfigLoader().load(PATH)


def test_json_load_error_is_propagated():
    # вариант из задания: имитируем ошибку разбора через patch('json.load')
    err = json.JSONDecodeError("Expecting value", "doc", 0)
    with patch("os.path.exists", return_value=True), \
            patch("builtins.open", mock_open(read_data="{}")), \
            patch("json.load", side_effect=err) as jl:
        with pytest.raises(json.JSONDecodeError):
            ConfigLoader().load(PATH)
    jl.assert_called_once()


def test_exists_error_is_propagated():
    with patch("os.path.exists", side_effect=OSError("I/O error")):
        with pytest.raises(OSError):
            ConfigLoader().load(PATH)


def test_file_handle_is_closed_after_read():
    m = mock_open(read_data="{}")
    with patch("os.path.exists", return_value=True), patch("builtins.open", m):
        ConfigLoader().load(PATH)
    m().__exit__.assert_called_once()               # with-блок корректно закрыл файл
