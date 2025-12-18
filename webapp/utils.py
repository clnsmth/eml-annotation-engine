import re
from collections import defaultdict

def extract_ontology(uri):
    """Parses the ontology code (ENVO, PATO, IAO, ECSO, DWC) from a URI."""
    if not uri:
        return "UNKNOWN"
    match = re.search(r'/obo/([A-Z]+)_', uri)
    if match:
        return match.group(1)
    match_ecso = re.search(r'/odo/(ECSO)_', uri)
    if match_ecso:
        return match_ecso.group(1)
    if "dwc/terms" in uri:
        return "DWC"
    return "UNKNOWN"

MERGE_CONFIG = {
    "ATTRIBUTE": {
        "property_label": "contains measurements of type",
        "property_uri": "http://ecoinformatics.org/oboe/oboe.1.2/oboe-core.owl#containsMeasurementsOfType",
        "join_key": "column_name"
    }
}

def merge_recommender_results(source_items, recommender_items, eml_type="ATTRIBUTE"):
    """
    Joins recommender response back to source items using 'column_name'.
    """
    config = MERGE_CONFIG.get(eml_type)
    if not config: return []

    rec_lookup = defaultdict(list)
    for rec in recommender_items:
        key = rec.get('column_name')
        if key:
            rec_lookup[key].append(rec)

    merged_results = []
    for item in source_items:
        match_val = item.get("name")
        if match_val in rec_lookup:
            entry = {
                "id": item['id'],
                "recommendations": []
            }
            for rec_data in rec_lookup[match_val]:
                annot = {
                    "label": rec_data['concept_name'],
                    "uri": rec_data['concept_id'],
                    "ontology": extract_ontology(rec_data['concept_id']),
                    "confidence": rec_data['confidence'],
                    "description": rec_data['concept_definition'],
                    "propertyLabel": config['property_label'],
                    "propertyUri": config['property_uri'],
                    "attributeName": item.get('name'),
                    "objectName": item.get('objectName')
                }
                entry["recommendations"].append(annot)
            merged_results.append(entry)
    return merged_results

def reformat_attribute_elements(attributes):
    """
    Transform attribute elements to the format expected by the attribute recommender.
    """
    reformatted = []
    for attr in attributes:
        reformatted.append({
            "entity_name": attr.get("objectName"),
            "entity_description": attr.get("entityDescription"),
            "object_name": attr.get("objectName"),
            "column_name": attr.get("name"),
            "column_description": attr.get("description"),
        })
    return reformatted

def reformat_geographic_coverage_elements(geos):
    """
    Stub: Transform geographic coverage elements to the format expected by the geographic coverage recommender.
    For now, returns input unchanged.
    """
    return geos
