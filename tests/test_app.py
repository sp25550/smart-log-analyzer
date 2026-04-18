import sys
import os
import tempfile

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import analyze_logs


def create_sample_log(content):
    temp = tempfile.NamedTemporaryFile(delete=False, mode="w")
    temp.write(content)
    temp.close()
    return temp.name


def test_error_count():
    log = """2026-04-18 10:00:01 ERROR Database failed
2026-04-18 10:01:01 ERROR Database failed
2026-04-18 10:02:01 INFO Server started"""

    file_path = create_sample_log(log)
    result = analyze_logs(file_path)

    assert result["errors"] == 2


def test_warning_count():
    log = """2026-04-18 10:00:01 WARNING Disk high
2026-04-18 10:01:01 WARNING CPU high"""

    file_path = create_sample_log(log)
    result = analyze_logs(file_path)

    assert result["warnings"] == 2


def test_info_count():
    log = """2026-04-18 10:00:01 INFO Start
2026-04-18 10:01:01 INFO Running"""

    file_path = create_sample_log(log)
    result = analyze_logs(file_path)

    assert result["infos"] == 2


def test_severity_detection():
    log = """2026-04-18 10:00:01 ERROR System crash detected"""

    file_path = create_sample_log(log)
    result = analyze_logs(file_path)

    assert result["logs"][0]["severity"] == "HIGH"


def test_empty_file():
    file_path = create_sample_log("")
    result = analyze_logs(file_path)

    assert result["total"] == 0


def test_mixed_logs():
    log = """2026-04-18 10:00:01 INFO Start
2026-04-18 10:01:01 WARNING Disk
2026-04-18 10:02:01 ERROR Fail"""

    file_path = create_sample_log(log)
    result = analyze_logs(file_path)

    assert result["errors"] == 1
    assert result["warnings"] == 1
    assert result["infos"] == 1


def test_top_error():
    log = """2026-04-18 10:00:01 ERROR DB failed
2026-04-18 10:01:01 ERROR DB failed
2026-04-18 10:02:01 ERROR Timeout"""

    file_path = create_sample_log(log)
    result = analyze_logs(file_path)

    assert result["top_errors"][0][0] == "DB failed"


def test_invalid_format():
    log = """INVALID LOG LINE"""

    file_path = create_sample_log(log)
    result = analyze_logs(file_path)

    assert result["total"] == 0


def test_low_severity():
    log = """2026-04-18 10:00:01 WARNING Disk high"""

    file_path = create_sample_log(log)
    result = analyze_logs(file_path)

    assert result["logs"][0]["severity"] == "LOW"


def test_medium_severity():
    log = """2026-04-18 10:00:01 ERROR Some error"""

    file_path = create_sample_log(log)
    result = analyze_logs(file_path)

    assert result["logs"][0]["severity"] == "MEDIUM"