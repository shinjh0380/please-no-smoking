from __future__ import annotations

from pathlib import Path

SPEC_PATH = Path(__file__).resolve().parent.parent / "please-no-smoking.spec"


class TestPackagingSpec:
    def test_spec_console_is_false(self) -> None:
        text = SPEC_PATH.read_text(encoding="utf-8")
        assert "console=False" in text, (
            "spec 파일에 console=False가 없습니다. "
            "--windowed 플래그 없이 빌드하면 콘솔창이 표시됩니다."
        )
