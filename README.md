# oca-cli

## Quickstart

```bash
# install the package
pip install oca-cli

# Create a sample schema file
SAMPLE_BUNDLE=$(cat <<EOF
{
    "name": "Sample",
    "description": "A sample bundle",
    "issuer": "Demo issuer",
    "attributes": [
        "first_name",
        "last_name"
    ]
}
EOF
)
echo $SAMPLE_BUNDLE > sample_schema.json

# Draft an OCA Bundle
oca draft -f sample_schema.json > sample_draft.json

# Edit the bundle then secure it
oca secure -f sample_draft.json > sample_bundle.json

```