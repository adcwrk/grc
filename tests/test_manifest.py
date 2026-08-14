from pathlib import Path

from scripts.build_manifest import build_manifest


def test_manifest_generation(tmp_path: Path) -> None:
    artifact = tmp_path / "clients" / "acme" / "evidence" / "evidence.md"
    artifact.parent.mkdir(parents=True)
    artifact.write_text(
        """---
artifact_id: EVID-0001
artifact_type: evidence
client: acme
framework:
  - Example
requirement:
  - EX-1
status: draft
sensitivity: INTERNAL
tags:
  - identity
---

# Evidence
""",
        encoding="utf-8",
    )

    manifest = build_manifest(tmp_path)

    assert manifest["artifact_count"] == 1
    assert manifest["artifacts"][0]["artifact_id"] == "EVID-0001"
    assert manifest["artifacts"][0]["path"] == "clients/acme/evidence/evidence.md"
