from app import clean_json_text, make_data_url, normalize_result


def test_clean_json_text_removes_markdown_fences():
    raw = '```json\n{"test": "Hemoglobin"}\n```'
    result = clean_json_text(raw)
    assert result == '{"test": "Hemoglobin"}'


def test_clean_json_text_extracts_json_object():
    raw = 'Here is the result:\n{"test": "Glucose"}\nDone.'
    result = clean_json_text(raw)
    assert result == '{"test": "Glucose"}'


def test_make_data_url():
    result = make_data_url(b"abc", "image/jpeg")
    assert result.startswith("data:image/jpeg;base64,")


def test_normalize_result_keeps_expected_structure():
    data = {
        "tests": [],
        "conflicts": [],
        "summary": "Test summary"
    }

    result = normalize_result(data)

    assert isinstance(result, dict)
    assert "tests" in result
    assert "conflicts" in result
    assert "summary" in result


def test_normalize_result_defaults_missing_sections():
    result = normalize_result({})

    assert isinstance(result, dict)
    assert "tests" in result
    assert "conflicts" in result
    assert "summary" in result
    assert isinstance(result["tests"], list)
    assert isinstance(result["conflicts"], list)
