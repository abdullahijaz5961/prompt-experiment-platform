from prompt_lab.core import health_summary

def test_health_summary():
    result = health_summary()
    assert result["status"] == "ok"
    assert result["project"]
