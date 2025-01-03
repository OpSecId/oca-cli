import base64
from blake3 import blake3
import jcs
import json
import re


class OCAProcessorError(Exception):
    """Generic OCAProcessor Error."""


class OCAProcessor:
    def __init__(self):
        self.dummy_string = "#" * 44

    def generate_said(self, value):
        # https://datatracker.ietf.org/doc/html/draft-ssmith-said#name-generation-and-verification
        # https://trustoverip.github.io/tswg-cesr-specification/#text-coding-scheme-design
        return "E" + (
            base64.urlsafe_b64encode(
                bytes([0]) + blake3(jcs.canonicalize(value)).digest()
            ).decode()
        ).lstrip("A")

    def secure_bundle(self, bundle):
        capture_base = bundle[0]
        overlays = capture_base.pop('overlays')
        
        capture_base["digest"] = self.dummy_string
        capture_base["digest"] = self.generate_said(capture_base)
        
        for idx, overlay in enumerate(overlays):
            overlays[idx]["capture_base"] = capture_base["digest"]
            overlays[idx]["digest"] = self.dummy_string
            overlays[idx]["digest"] = self.generate_said(overlays[idx])

        secures_bundle = [capture_base | {"overlays": overlays}]
        return secures_bundle

    def draft_bundle(self, schema):
        capture_base = {
            "type": "spec/capture_base/1.0",
            "attributes": {attribute: 'Text' for attribute in schema['attributes']},
            "flagged_attributes": [],
            'overlays': []
        }
        encoding = {
            "type": "spec/overlays/character_encoding/1.0",
            "default_character_encoding": "utf-8",
            "attribute_character_encoding": {attribute: "utf-8" for attribute in schema['attributes']},
        }
        capture_base['overlays'].append(encoding)
        
        labels = {
            "type": "spec/overlays/label/1.0",
            "lang": "en",
            "attribute_labels": {attribute: attribute.replace('_', ' ').capitalize() for attribute in schema['attributes']},
        }
        capture_base['overlays'].append(labels)
        
        information = {
            "type": "spec/overlays/information/1.0",
            "lang": "en",
            "attribute_information": {attribute: 'Lorem ipsum' for attribute in schema['attributes']},
        }
        capture_base['overlays'].append(information)
        
        meta = {
            "type": "spec/overlays/meta/1.0",
            "language": "en",
            "issuer": schema["name"],
            "name": schema["name"],
            "description": schema['description'],
            "credential_help_text": "Learn more",
            "credential_support_url": ""
        }
        capture_base['overlays'].append(meta)
        
        branding = {
            "type": "aries/overlays/branding/1.0",
            "logo": "",
            "background_image": "",
            "background_image_slice": "",
            "primary_background_color": "",
            "secondary_background_color": "",
            "primary_attribute": "",
            "secondary_attribute": "",
            "expiry_date_attribute": "",
        }
        capture_base['overlays'].append(branding)
        return [capture_base]

    def create_bundle(self, credential_registration, credential_template):
        capture_base = {
            "type": "spec/capture_base/1.0",
            "attributes": {},
            "flagged_attributes": [],
            "digest": self.dummy_string,
        }
        labels = {
            "type": "spec/overlays/label/1.0",
            "lang": "en",
            "attribute_labels": {},
        }
        information = {
            "type": "spec/overlays/information/1.0",
            "lang": "en",
            "attribute_information": {},
        }
        meta = {
            "type": "spec/overlays/meta/1.0",
            "language": "en",
            "issuer": credential_template["issuer"]["name"],
            "name": credential_template["name"],
            # "description": credential_template['description'],
        }

        branding = {
            "type": "aries/overlays/branding/1.0",
            "primary_attribute": "entityId",
            "secondary_attribute": "cardinalityId",
            "primary_background_color": "#003366",
            "secondary_background_color": "#00264D",
            "logo": "https://avatars.githubusercontent.com/u/916280",
        }
        paths = {"type": "vc/overlays/path/1.0", "attribute_paths": {}}
        clusters = {
            "type": "vc/overlays/cluster/1.0",
            "lang": "en",
            "attribute_clusters": {},
        }
        attributes = (
            credential_registration["corePaths"]
            | credential_registration["subjectPaths"]
        )
        for attribute in attributes:
            capture_base["attributes"][attribute] = "Text"
            labels["attribute_labels"][attribute] = " ".join(
                re.findall("[A-Z][^A-Z]*", attribute)
            ).upper()
            paths["attribute_paths"][attribute] = attributes[attribute]

        overlays = [
            labels,
            # information,
            meta,
            branding,
            paths,
            # clusters,
        ]

        capture_base["digest"] = self.generate_said(capture_base)
        for idx, overlay in enumerate(overlays):
            overlays[idx]["capture_base"] = capture_base["digest"]
            overlays[idx]["digest"] = self.dummy_string
            overlays[idx]["digest"] = self.generate_said(overlays[idx])

        bundle = capture_base | {"overlays": overlays}
        return bundle

    def get_overlay(self, bundle, overlay_type):
        return next(
            (
                overlay
                for overlay in bundle["overlays"]
                if overlay["type"] == overlay_type
            ),
            None,
        )