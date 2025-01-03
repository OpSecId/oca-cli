
from typer.testing import CliRunner

from oca.processor import OCAProcessor

runner = CliRunner()

SCHEMA = {
    "name": "Sample",
    "description": "A sample bundle",
    "issuer": "Demo issuer",
    "attributes": [
        "first_name",
        "last_name"
    ]
}

def test_drafting():
    drafted_bundle = OCAProcessor().draft_bundle(SCHEMA)
    assert drafted_bundle

def test_securing():
    drafted_bundle = OCAProcessor().draft_bundle(SCHEMA)
    secured_bundle = OCAProcessor().secure_bundle(drafted_bundle)
    assert secured_bundle