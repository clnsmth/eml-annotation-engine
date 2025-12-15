from webapp.run import (
    recommend_for_attribute,
    recommend_for_geographic_coverage,
    reformat_attribute_elements,
    reformat_geographic_coverage_elements,
    parse_eml_elements,
    app,
)
from fastapi.testclient import TestClient

client = TestClient(app)


# --- Unit tests for individual recommenders ---
def test_recommend_for_attribute_unit():
    """
    Unit test for recommend_for_attribute.
    """
    attributes = [
        {"name": "SurveyID", "type": "string"},
        {"name": "SampleID", "type": "int"},
    ]
    results = recommend_for_attribute(attributes)
    assert isinstance(results, list)
    assert len(results) == 2
    for i, item in enumerate(results):
        assert item["id"] == f"attribute-{i}"
        assert "recommendations" in item
        rec = item["recommendations"][0]
        assert rec["label"] == "Identifier"
        assert rec["ontology"] == "IAO"


def test_recommend_for_geographic_coverage_unit():
    """
    Unit test for recommend_for_geographic_coverage.
    """
    geos = [
        {"description": "Lake Tahoe region", "objectName": "LakeTahoe"},
        {"description": "Sierra Nevada", "objectName": "SierraNevada"},
    ]
    results = recommend_for_geographic_coverage(geos)
    assert isinstance(results, list)
    assert len(results) == 2
    for i, item in enumerate(results):
        assert item["id"] == f"geographicCoverage-{i}"
        assert "recommendations" in item
        rec = item["recommendations"][0]
        assert rec["label"] == "Geographic Region"
        assert rec["ontology"] == "ENVO"
        assert rec["attributeName"] == geos[i]["description"]
        assert rec["objectName"] == geos[i]["objectName"]


def test_parse_eml_elements_unit():
    """
    Unit test for parse_eml_elements, now ensures reformatting is applied using the mock frontend payload.
    """
    payload = {"elements": {
        "attribute": MOCK_FRONTEND_PAYLOAD["ATTRIBUTE"],
        "geographicCoverage": MOCK_FRONTEND_PAYLOAD["COVERAGE"]
    }}
    grouped = parse_eml_elements(payload)
    assert set(grouped.keys()) == {"attribute", "geographicCoverage"}
    assert grouped["attribute"] == reformat_attribute_elements(MOCK_FRONTEND_PAYLOAD["ATTRIBUTE"])
    assert grouped["geographicCoverage"] == reformat_geographic_coverage_elements(MOCK_FRONTEND_PAYLOAD["COVERAGE"])


def test_reformat_attribute_elements_unit():
    from webapp.run import reformat_attribute_elements
    data = [
        {
            "id": "d49be2c0-7b9e-41f4-ae07-387d3e1f14c8",
            "name": "Latitude",
            "description": "Latitude of collection",
            "context": "SurveyResults",
            "objectName": "SurveyResults.csv",
            "entityDescription": "Table contains survey information and the counts of the number of egg masses for each species during that survey."
        }
    ]
    expected = [
        {
            "entity_name": "SurveyResults.csv",
            "entity_description": "Table contains survey information and the counts of the number of egg masses for each species during that survey.",
            "object_name": "SurveyResults.csv",
            "column_name": "Latitude",
            "column_description": "Latitude of collection"
        }
    ]
    out = reformat_attribute_elements(data)
    assert out == expected


def test_reformat_geographic_coverage_elements_unit():
    from webapp.run import reformat_geographic_coverage_elements
    data = [{"description": "D1"}, {"description": "D2"}]
    out = reformat_geographic_coverage_elements(data)
    assert out == data


# --- Integration tests for the endpoint (keep only those that test the endpoint as a whole) ---
def test_recommendations_endpoint():
    # Minimal example EML metadata payload using a supported type key
    payload = {"elements": {"attribute": [
        {"name": "SurveyID", "type": "string"}
    ]}}
    response = client.post("/api/recommendations", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    # Check that each item has 'id' and 'recommendations' keys
    for item in data:
        assert "id" in item
        assert "recommendations" in item
        assert isinstance(item["recommendations"], list)
        # Check that each recommendation has required keys
        for rec in item["recommendations"]:
            assert "label" in rec
            assert "uri" in rec
            assert "ontology" in rec
            assert "confidence" in rec
            assert "description" in rec
            assert "propertyLabel" in rec
            assert "propertyUri" in rec
            # Optional keys: attributeName, objectName (may not be present in all)


# --- Example mock POST JSON payload from frontend (to be filled in by user) ---
MOCK_FRONTEND_PAYLOAD = {
    "DATATABLE": [
        {
            "id": "24632bb8dbdace8be4693baf5c9e4b97",
            "name": "SurveyResults",
            "description": "Table contains survey information and the counts of the number of egg masses for each species during that survey.",
            "context": "SurveyResults",
            "objectName": "SurveyResults.csv",
            "entityDescription": "Table contains survey information and the counts of the number of egg masses for each species during that survey."
        },
        {
            "id": "9f81741eef929975361d53fe07d370b9",
            "name": "EggMasses",
            "description": "Contains fine-scale information on groups of egg masses encountered during a survey, including GPS data. These data were only collected from 2021 onward, and were not collected for every survey--SurveyResults has the authoritative counts of egg masses for each survey.",
            "context": "EggMasses",
            "objectName": "EggMasses.csv",
            "entityDescription": "Contains fine-scale information on groups of egg masses encountered during a survey, including GPS data. These data were only collected from 2021 onward, and were not collected for every survey--SurveyResults has the authoritative counts of egg masses for each survey."
        }
    ],
    "ATTRIBUTE": [
        {
            "id": "cfe0601b-e76b-4f34-8a5a-655db3b0491c",
            "name": "SurveyID",
            "description": "Unique ID based on date and lake surveyesd",
            "context": "SurveyResults",
            "objectName": "SurveyResults.csv",
            "entityDescription": "Table contains survey information and the counts of the number of egg masses for each species during that survey."
        },
        {
            "id": "d49be2c0-7b9e-41f4-ae07-387d3e1f14c8",
            "name": "Latitude",
            "description": "Latitude of collection",
            "context": "SurveyResults",
            "objectName": "SurveyResults.csv",
            "entityDescription": "Table contains survey information and the counts of the number of egg masses for each species during that survey."
        },
        {
            "id": "d2569832-42ec-4532-b333-bf68e84598da",
            "name": "Longitude",
            "description": "longitude of collection",
            "context": "SurveyResults",
            "objectName": "SurveyResults.csv",
            "entityDescription": "Table contains survey information and the counts of the number of egg masses for each species during that survey."
        },
        {
            "id": "81506c28-3ae9-473a-8426-70117c4a84ac",
            "name": "Accuracy_m",
            "description": "GPS positional accuracy in meters, as reported by iphone data collection app",
            "context": "SurveyResults",
            "objectName": "SurveyResults.csv",
            "entityDescription": "Table contains survey information and the counts of the number of egg masses for each species during that survey."
        },
        {
            "id": "6778d3cd-77e3-4b7b-9844-31248310479d",
            "name": "Date",
            "description": "sampling date. If the sampling date is March 1st of any given year, this is a placeholder date for a survey year where no survey date was recorded.",
            "context": "SurveyResults",
            "objectName": "SurveyResults.csv",
            "entityDescription": "Table contains survey information and the counts of the number of egg masses for each species during that survey."
        },
        {
            "id": "6464d56e-8a40-4962-ae4c-1cbc7795250e",
            "name": "StartTime",
            "description": "Start time of survey in Pacific Time (America/LosAngeles), with appropriate daylight savings adjustment, if applicable",
            "context": "SurveyResults",
            "objectName": "SurveyResults.csv",
            "entityDescription": "Table contains survey information and the counts of the number of egg masses for each species during that survey."
        },
        {
            "id": "be22b649-5e4e-43bd-ad37-1965f3d23bdc",
            "name": "EndTime",
            "description": "End time of survey in Pacific Time (America/LosAngeles), with appropriate daylight savings adjustment, if applicable",
            "context": "SurveyResults",
            "objectName": "SurveyResults.csv",
            "entityDescription": "Table contains survey information and the counts of the number of egg masses for each species during that survey."
        },
        {
            "id": "3132391c-2f62-4aac-a208-549c2cbff735",
            "name": "SurveyLength",
            "description": "Total time spent on survey (HH:MM)",
            "context": "SurveyResults",
            "objectName": "SurveyResults.csv",
            "entityDescription": "Table contains survey information and the counts of the number of egg masses for each species during that survey."
        },
        {
            "id": "e58a1ac7-066f-45f9-a4b8-9b596c60eb07",
            "name": "SurveyLengthCalc",
            "description": "Total time spent on survey (HH:MM), estimated when end time was not recorded, based off of the last observation time during that survey.",
            "context": "SurveyResults",
            "objectName": "SurveyResults.csv",
            "entityDescription": "Table contains survey information and the counts of the number of egg masses for each species during that survey."
        },
        {
            "id": "f31e76c5-3359-4b21-af25-9e09634ab47f",
            "name": "latest_observation_time",
            "description": "The final egg mass detection time in a survey-used for SurveyLengthCalc.",
            "context": "SurveyResults",
            "objectName": "SurveyResults.csv",
            "entityDescription": "Table contains survey information and the counts of the number of egg masses for each species during that survey."
        },
        {
            "id": "66c5e93d-7a8b-4dbf-989f-9294db3ec7b9",
            "name": "Lake",
            "description": "Lake surveyed. Big Lake and Deep Lake form one continuous waterbody during high water years, and from 2021 to 2022 it was surveyed as one lake as opposed to breaking the lake up into two surveys. See map jpg for lake name labels.",
            "context": "SurveyResults",
            "objectName": "SurveyResults.csv",
            "entityDescription": "Table contains survey information and the counts of the number of egg masses for each species during that survey."
        },
        {
            "id": "398be849-a3d4-4c61-9013-ae41cb6d6d59",
            "name": "Observer",
            "description": "Last name, or first and last name, of surveyor(s)",
            "context": "SurveyResults",
            "objectName": "SurveyResults.csv",
            "entityDescription": "Table contains survey information and the counts of the number of egg masses for each species during that survey."
        },
        {
            "id": "88da6649-63cf-4b6f-a3c8-6a37a6155833",
            "name": "Sky",
            "description": "Cloud cover characteristics at the start of the survey. Egg masses are easier to see in clear and sunny conditions compared to overcast and cloudy conditions.",
            "context": "SurveyResults",
            "objectName": "SurveyResults.csv",
            "entityDescription": "Table contains survey information and the counts of the number of egg masses for each species during that survey."
        },
        {
            "id": "56fb8aad-a34a-4ebb-9175-bf80b2f6840f",
            "name": "Precip",
            "description": "Precipitation at the survey start. Rain disturbs the water surface and makes egg masses difficult to see.",
            "context": "SurveyResults",
            "objectName": "SurveyResults.csv",
            "entityDescription": "Table contains survey information and the counts of the number of egg masses for each species during that survey."
        },
        {
            "id": "3357918a-e3b9-4829-97cc-f44b1aa6b51e",
            "name": "Wind",
            "description": "General description of wind at start of survey. Wind disturbs the water surface and makes egg masses harder to see.",
            "context": "SurveyResults",
            "objectName": "SurveyResults.csv",
            "entityDescription": "Table contains survey information and the counts of the number of egg masses for each species during that survey."
        },
        {
            "id": "71c4f9e8-5448-4d5b-859a-1b6b6bc2dd46",
            "name": "AirThermometer",
            "description": "Check if a thermometer was used to measure air temperature in the field.",
            "context": "SurveyResults",
            "objectName": "SurveyResults.csv",
            "entityDescription": "Table contains survey information and the counts of the number of egg masses for each species during that survey."
        },
        {
            "id": "0673eb41-1b47-4d32-9d87-bf10e17c69b6",
            "name": "AirTemperature_F",
            "description": "Air temperature measured at the start of the survey (if airthermometer=Yes), or from cell phone weather app",
            "context": "SurveyResults",
            "objectName": "SurveyResults.csv",
            "entityDescription": "Table contains survey information and the counts of the number of egg masses for each species during that survey."
        },
        {
            "id": "0ade98ad-add4-4ce5-afcb-6c703b12cf1e",
            "name": "WaterThermometer",
            "description": "Check if a thermometer was used to measure water temperature in the field.",
            "context": "SurveyResults",
            "objectName": "SurveyResults.csv",
            "entityDescription": "Table contains survey information and the counts of the number of egg masses for each species during that survey."
        },
        {
            "id": "dca8c4a4-472b-4998-bf35-82b9e4fb8f22",
            "name": "WaterTemperature_F",
            "description": "Water temperature measured at the start of the survey at 6 inch depth, in the shade if possible.",
            "context": "SurveyResults",
            "objectName": "SurveyResults.csv",
            "entityDescription": "Table contains survey information and the counts of the number of egg masses for each species during that survey."
        },
        {
            "id": "7713a0b2-d5b2-4378-8d6d-6c74baae6971",
            "name": "WaterColor",
            "description": "Color of the lake water (clear, or stained from tannins). Egg masses slightly harder to discern in stained water.",
            "context": "SurveyResults",
            "objectName": "SurveyResults.csv",
            "entityDescription": "Table contains survey information and the counts of the number of egg masses for each species during that survey."
        },
        {
            "id": "62090101-5cc1-463c-a63d-843616d148cb",
            "name": "SurveyType",
            "description": "Conveyance method for the survey.",
            "context": "SurveyResults",
            "objectName": "SurveyResults.csv",
            "entityDescription": "Table contains survey information and the counts of the number of egg masses for each species during that survey."
        },
        {
            "id": "0c944fd1-915e-40fb-82f1-b2da8a5da74e",
            "name": "Comments",
            "description": "Freeform comments about the survey",
            "context": "SurveyResults",
            "objectName": "SurveyResults.csv",
            "entityDescription": "Table contains survey information and the counts of the number of egg masses for each species during that survey."
        },
        {
            "id": "24b4badd-56b7-4dbf-8848-f6531f20c024",
            "name": "SpeciesCode",
            "description": "Species code identifier for the NumberOf... columns",
            "context": "SurveyResults",
            "objectName": "SurveyResults.csv",
            "entityDescription": "Table contains survey information and the counts of the number of egg masses for each species during that survey."
        },
        {
            "id": "60ffc8a2-c42f-40ab-89fa-db294f256e50",
            "name": "NumberOfEggMasses",
            "description": "Number of egg masses counted per species during a survey",
            "context": "SurveyResults",
            "objectName": "SurveyResults.csv",
            "entityDescription": "Table contains survey information and the counts of the number of egg masses for each species during that survey."
        },
        {
            "id": "6630e2e6-ed6e-4d50-8fdb-b9eff7e905cf",
            "name": "NumberOfAdults",
            "description": "Number of adults counted per species during a survey",
            "context": "SurveyResults",
            "objectName": "SurveyResults.csv",
            "entityDescription": "Table contains survey information and the counts of the number of egg masses for each species during that survey."
        },
        {
            "id": "4403ca82-f7e0-48c8-8cef-ca07017f4d2b",
            "name": "Weather",
            "description": "longform description of weather conditions",
            "context": "SurveyResults",
            "objectName": "SurveyResults.csv",
            "entityDescription": "Table contains survey information and the counts of the number of egg masses for each species during that survey."
        },
        {
            "id": "8a90023e-72cc-4540-a4b2-d4532ea86c38",
            "name": "SurveyID",
            "description": "Unique ID based on date and lake surveyed",
            "context": "EggMasses",
            "objectName": "EggMasses.csv",
            "entityDescription": "Contains fine-scale information on groups of egg masses encountered during a survey, including GPS data. These data were only collected from 2021 onward, and were not collected for every survey--SurveyResults has the authoritative counts of egg masses for each survey."
        },
        {
            "id": "c36d17e7-89b2-4722-b586-49d9934a398e",
            "name": "DateTime",
            "description": "Date and time of observation of egg mass(es). America/LosAngeles time zone.",
            "context": "EggMasses",
            "objectName": "EggMasses.csv",
            "entityDescription": "Contains fine-scale information on groups of egg masses encountered during a survey, including GPS data. These data were only collected from 2021 onward, and were not collected for every survey--SurveyResults has the authoritative counts of egg masses for each survey."
        },
        {
            "id": "2a325933-956f-485f-b0be-2817f7b7462c",
            "name": "Latitude",
            "description": "Latitude of observation (WGS84)",
            "context": "EggMasses",
            "objectName": "EggMasses.csv",
            "entityDescription": "Contains fine-scale information on groups of egg masses encountered during a survey, including GPS data. These data were only collected from 2021 onward, and were not collected for every survey--SurveyResults has the authoritative counts of egg masses for each survey."
        },
        {
            "id": "d9a40fb9-4210-4527-9f4f-219c3583ef1c",
            "name": "Longitude",
            "description": "Longitude of observation (WGS84",
            "context": "EggMasses",
            "objectName": "EggMasses.csv",
            "entityDescription": "Contains fine-scale information on groups of egg masses encountered during a survey, including GPS data. These data were only collected from 2021 onward, and were not collected for every survey--SurveyResults has the authoritative counts of egg masses for each survey."
        },
        {
            "id": "1e536558-938d-45a8-b83d-5d178cfd7d18",
            "name": "Accuracy_m",
            "description": "Estimated GPS precision",
            "context": "EggMasses",
            "objectName": "EggMasses.csv",
            "entityDescription": "Contains fine-scale information on groups of egg masses encountered during a survey, including GPS data. These data were only collected from 2021 onward, and were not collected for every survey--SurveyResults has the authoritative counts of egg masses for each survey."
        },
        {
            "id": "85b6fa31-21ce-4e3a-a8f7-404c669a9cc7",
            "name": "NumberOfEggMasses",
            "description": "The number of egg masses counted in a given observation. Nearby egg masses of the same species and on the same substrate were grouped together in one observation to speed data entry. Those egg masses were often within a couple meters of each other.",
            "context": "EggMasses",
            "objectName": "EggMasses.csv",
            "entityDescription": "Contains fine-scale information on groups of egg masses encountered during a survey, including GPS data. These data were only collected from 2021 onward, and were not collected for every survey--SurveyResults has the authoritative counts of egg masses for each survey."
        },
        {
            "id": "f838b7b8-2468-47bd-9717-56ea091e4780",
            "name": "SpeciesCode",
            "description": "Amphibian species of the egg mass observation",
            "context": "EggMasses",
            "objectName": "EggMasses.csv",
            "entityDescription": "Contains fine-scale information on groups of egg masses encountered during a survey, including GPS data. These data were only collected from 2021 onward, and were not collected for every survey--SurveyResults has the authoritative counts of egg masses for each survey."
        },
        {
            "id": "3220828d-a9a3-4c98-89a6-36f4a740a57e",
            "name": "EggMassSubstrate",
            "description": "What the egg mass was attached to",
            "context": "EggMasses",
            "objectName": "EggMasses.csv",
            "entityDescription": "Contains fine-scale information on groups of egg masses encountered during a survey, including GPS data. These data were only collected from 2021 onward, and were not collected for every survey--SurveyResults has the authoritative counts of egg masses for each survey."
        },
        {
            "id": "8854db34-3d6e-481a-81d4-a73a6b3eb8b1",
            "name": "Comments",
            "description": "comments about the observation",
            "context": "EggMasses",
            "objectName": "EggMasses.csv",
            "entityDescription": "Contains fine-scale information on groups of egg masses encountered during a survey, including GPS data. These data were only collected from 2021 onward, and were not collected for every survey--SurveyResults has the authoritative counts of egg masses for each survey."
        }
    ],
    "OTHERENTITY": [
        {
            "id": "befe3d845aea4510048251bd0079e3de",
            "name": "14LakesRiparianHabitatRestorationProjectAsBuilt2012",
            "description": "14 Lakes Riparian Habitat Restoration Project As-Built Document referenced in SurveyReport_2003_2014 amphibian monitoring survey report. Provided for greater context regarding habitat management in the project location.",
            "context": "14LakesRiparianHabitatRestorationProjectAsBuilt2012",
            "objectName": "14LakesRiparianHabitatRestorationProjectAsBuilt2012.pdf",
            "entityDescription": "14 Lakes Riparian Habitat Restoration Project As-Built Document referenced in SurveyReport_2003_2014 amphibian monitoring survey report. Provided for greater context regarding habitat management in the project location."
        }
    ],
    "COVERAGE": [
        {
            "id": "geo-1",
            "name": "Location",
            "description": "A series of small lakes within the Cedar River Municipal Watershed in the Puget Sound region of western Washington State, USA",
            "context": "Geographic Coverage"
        }
    ]
}


def test_formatters_with_mock_frontend_payload():
    """
    Test the formatter functions using the example mock POST JSON payload from the frontend.
    This is a placeholder; user should fill in MOCK_FRONTEND_PAYLOAD with real data.
    """
    if not MOCK_FRONTEND_PAYLOAD:
        import pytest
        pytest.skip("No mock frontend payload provided.")
    grouped = parse_eml_elements(MOCK_FRONTEND_PAYLOAD)
    # For each group, call the corresponding formatter and check output type
    for group, items in grouped.items():
        if group == "attribute":
            assert isinstance(reformat_attribute_elements(items), list)
        elif group == "geographicCoverage":
            assert isinstance(reformat_geographic_coverage_elements(items), list)


def test_parse_eml_elements_with_mock_frontend_payload():
    """
    Test parse_eml_elements to ensure it uses reformat_attribute_elements correctly with the mock frontend payload.
    """
    # Use only the ATTRIBUTE group for clarity
    payload = {"elements": {"attribute": MOCK_FRONTEND_PAYLOAD["ATTRIBUTE"]}}
    grouped = parse_eml_elements(payload)
    # The 'attribute' group should be a list of reformatted items
    assert "attribute" in grouped
    reformatted = grouped["attribute"]
    # Each item in reformatted should match the output of reformat_attribute_elements
    expected = reformat_attribute_elements(MOCK_FRONTEND_PAYLOAD["ATTRIBUTE"])
    assert reformatted == expected

