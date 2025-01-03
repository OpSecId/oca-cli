import typer
import json
from typing_extensions import Annotated
from oca.processor import OCAProcessor

cli = typer.Typer()

@cli.command()
def draft(
    file: Annotated[str, typer.Option(
        '-f', '--file',
        help="Schema file name.",
        prompt=True
    )] = 'samples/schema.json'
    ):
    """Draft an OCA Bundle.
    """
    with open(file, 'r') as f:
        schema = json.loads(f.read())

    drafted_bundle = OCAProcessor().draft_bundle(schema)
    print(json.dumps(drafted_bundle, indent=2))

@cli.command()
def secure(
    file: Annotated[str, typer.Option(
        '-f', '--file',
        help="OCA Bundle file name.",
        prompt=True
    )] = 'samples/bundle.json'
    ):
    """Secure an OCA Bundle.
    """
    with open(file, 'r') as f:
        bundle = json.loads(f.read())

    secured_bundle = OCAProcessor().secure_bundle(bundle)
    print(json.dumps(secured_bundle, indent=2))

if __name__ == "__main__":
    typer.run(cli)