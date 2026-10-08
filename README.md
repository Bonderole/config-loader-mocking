# Мокирование файловой системы: ConfigLoader (ПР4, вариант 4)

Тестируется `ConfigLoader.load(path)` из `src/service.py` – чтение конфигурации из JSON-файла.
Реальные файлы в тестах не используются: `open()` заменяется на `mock_open`, `os.path.exists` и `json.load` – на `patch`.

## Запуск
```bash
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
pytest tests/ -v                                               # тесты
pytest tests --cov=src --cov-branch --cov-report=term-missing  # покрытие
experiments/run.sh                                             # ручные мутанты и рефакторинг
```

## Что проверяется
| Сценарий | Тест |
|---|---|
| успешная загрузка | `test_load_success`, `test_load_various_valid_contents` |
| корень JSON – не объект | `test_load_non_object_json_is_returned_as_is` |
| файл отсутствует | `test_file_not_found` |
| нет прав доступа | `test_permission_denied` |
| путь – каталог | `test_path_is_directory` |
| некорректный JSON | `test_invalid_json_content`, `test_json_load_error_is_propagated` |
| ошибка проверки существования | `test_exists_error_is_propagated` |
| файл закрыт после чтения | `test_file_handle_is_closed_after_read` |

## Структура
- `src/service.py` – тестируемый код (не изменялся)
- `tests/test_service.py` – тесты (16 случаев)
- `experiments/` – ручные мутанты кода и вариант на `pathlib`
- `results/` – вывод запусков (`pytest_v.txt`, `coverage.txt`, `experiments.txt`)
- `report.md` – анализ подхода, выводы, ответы на контрольные вопросы
