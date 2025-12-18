ORIGINAL_MOCK_RESPONSE = [
    {
        "id": "24632bb8dbdace8be4693baf5c9e4b97",
        "recommendations": [
            {
                "label": "Survey Dataset",
                "uri": "http://purl.obolibrary.org/obo/IAO_0000100",
                "ontology": "IAO",
                "confidence": 0.90,
                "description": "A data set that is a collection of data about a survey.",
                "propertyLabel": "contains",
                "propertyUri": "http://www.w3.org/ns/oa#hasBody",
            }
        ],
    },
    {
        "id": "cfe0601b-e76b-4f34-8a5a-655db3b0491c",
        "recommendations": [
            {
                "label": "Identifier",
                "uri": "http://purl.obolibrary.org/obo/IAO_0000578",
                "ontology": "IAO",
                "confidence": 0.95,
                "description": "An information content entity that identifies something.",
                "propertyLabel": "contains measurements of type",
                "propertyUri": "http://ecoinformatics.org/oboe/oboe.1.2/oboe-core.owl#containsMeasurementsOfType",
                "attributeName": "SurveyID",
                "objectName": "SurveyResults.csv",
            }
        ],
    },
    {
        "id": "d49be2c0-7b9e-41f4-ae07-387d3e1f14c8",
        "recommendations": [
            {
                "label": "Latitude",
                "uri": "http://purl.obolibrary.org/obo/GEO_00000016",
                "ontology": "GEO",
                "confidence": 0.99,
                "description": "The angular distance of a place north or south of the earth's equator.",
                "propertyLabel": "contains measurements of type",
                "propertyUri": "http://ecoinformatics.org/oboe/oboe.1.2/oboe-core.owl#containsMeasurementsOfType",
                "attributeName": "Latitude",
                "objectName": "SurveyResults.csv",
            }
        ],
    },
    {
        "id": "0673eb41-1b47-4d32-9d87-bf10e17c69b6",
        "recommendations": [
            {
                "label": "Air Temperature",
                "uri": "http://purl.obolibrary.org/obo/ENVO_00002006",
                "ontology": "ENVO",
                "confidence": 0.90,
                "description": "The temperature of the air.",
                "propertyLabel": "contains measurements of type",
                "propertyUri": "http://ecoinformatics.org/oboe/oboe.1.2/oboe-core.owl#containsMeasurementsOfType",
                "attributeName": "AirTemperature_F",
                "objectName": "SurveyResults.csv",
            },
            {
                "label": "Temperature",
                "uri": "http://purl.obolibrary.org/obo/PATO_0000146",
                "ontology": "PATO",
                "confidence": 0.85,
                "description": "A physical quality of the thermal energy of a system.",
                "propertyLabel": "contains measurements of type",
                "propertyUri": "http://ecoinformatics.org/oboe/oboe.1.2/oboe-core.owl#containsMeasurementsOfType",
                "attributeName": "AirTemperature_F",
                "objectName": "SurveyResults.csv",
            },
        ],
    },
    {
        "id": "dca8c4a4-472b-4998-bf35-82b9e4fb8f22",
        "recommendations": [
            {
                "label": "Water Temperature",
                "uri": "http://purl.obolibrary.org/obo/ENVO_00002010",
                "ontology": "ENVO",
                "confidence": 0.95,
                "description": "The temperature of water.",
                "propertyLabel": "contains measurements of type",
                "propertyUri": "http://ecoinformatics.org/oboe/oboe.1.2/oboe-core.owl#containsMeasurementsOfType",
                "attributeName": "WaterTemperature_F",
                "objectName": "SurveyResults.csv",
            }
        ],
    },
    {
        "id": "66c5e93d-7a8b-4dbf-989f-9294db3ec7b9",
        "recommendations": [
            {
                "label": "Lake",
                "uri": "http://purl.obolibrary.org/obo/ENVO_00000020",
                "ontology": "ENVO",
                "confidence": 0.92,
                "description": "A large body of water surrounded by land.",
                "propertyLabel": "contains measurements of type",
                "propertyUri": "http://ecoinformatics.org/oboe/oboe.1.2/oboe-core.owl#containsMeasurementsOfType",
                "attributeName": "Lake",
                "objectName": "SurveyResults.csv",
            }
        ],
    },
    {
        "id": "24b4badd-56b7-4dbf-8848-f6531f20c024",
        "recommendations": [
            {
                "label": "Taxon",
                "uri": "http://rs.tdwg.org/dwc/terms/Taxon",
                "ontology": "DWC",
                "confidence": 0.88,
                "description": "A group of one or more populations of an organism.",
                "propertyLabel": "contains measurements of type",
                "propertyUri": "http://ecoinformatics.org/oboe/oboe.1.2/oboe-core.owl#containsMeasurementsOfType",
                "attributeName": "SpeciesCode",
                "objectName": "SurveyResults.csv",
            },
            {
                "label": "Scientific Name",
                "uri": "http://rs.tdwg.org/dwc/terms/scientificName",
                "ontology": "DWC",
                "confidence": 0.80,
                "description": "The full scientific name.",
                "propertyLabel": "contains measurements of type",
                "propertyUri": "http://ecoinformatics.org/oboe/oboe.1.2/oboe-core.owl#containsMeasurementsOfType",
                "attributeName": "SpeciesCode",
                "objectName": "SurveyResults.csv",
            },
        ],
    },
    {
        "id": "3220828d-a9a3-4c98-89a6-36f4a740a57e",
        "recommendations": [
            {
                "label": "Surface Layer",
                "uri": "http://purl.obolibrary.org/obo/ENVO_00002005",
                "ontology": "ENVO",
                "confidence": 0.70,
                "description": "The layer of a material that is in contact with the surrounding medium.",
                "propertyLabel": "contains measurements of type",
                "propertyUri": "http://ecoinformatics.org/oboe/oboe.1.2/oboe-core.owl#containsMeasurementsOfType",
                "attributeName": "EggMassSubstrate",
                "objectName": "EggMasses.csv",
            }
        ],
    },
    {
        "id": "geo-1",
        "recommendations": [
            {
                "label": "Freshwater Lake Ecosystem",
                "uri": "http://purl.obolibrary.org/obo/ENVO_01000021",
                "ontology": "ENVO",
                "confidence": 0.75,
                "description": "An aquatic ecosystem that is part of a lake.",
                "propertyLabel": "contains",
                "propertyUri": "http://www.w3.org/ns/oa#hasBody",
            },
            {
                "label": "Temperate Climate",
                "uri": "http://purl.obolibrary.org/obo/ENVO_01000000",
                "ontology": "ENVO",
                "confidence": 0.80,
                "description": "A climate with moderate conditions",
                "propertyLabel": "contains",
                "propertyUri": "http://www.w3.org/ns/oa#hasBody",
            },
        ],
    },
    {
        "id": "befe3d845aea4510048251bd0079e3de",
        "recommendations": [
            {
                "label": "Technical Report",
                "uri": "http://purl.obolibrary.org/obo/IAO_0000088",
                "ontology": "IAO",
                "confidence": 0.85,
                "description": "A report concerning the results of a scientific investigation or technical development.",
                "propertyLabel": "contains",
                "propertyUri": "http://www.w3.org/ns/oa#hasBody",
            }
        ],
    },
]

# Changed to a Dictionary keyed by ObjectName
MOCK_ATTRIBUTE_RECOMMENDATIONS_BY_FILE = {
    "SurveyResults.csv": [
        {
            "column_name": "SurveyID",
            "concept_name": "Identifier",
            "concept_definition": "An information content entity that identifies something.",
            "concept_id": "http://purl.obolibrary.org/obo/IAO_0000578",
            "confidence": 0.95
        },
        {
            "column_name": "Latitude",
            "concept_name": "Latitude",
            "concept_definition": "The angular distance of a place north or south of the earth's equator.",
            "concept_id": "http://purl.obolibrary.org/obo/GEO_00000016",
            "confidence": 0.99
        },
        {
            "column_name": "AirTemperature_F",
            "concept_name": "Air Temperature",
            "concept_definition": "The temperature of the air.",
            "concept_id": "http://purl.obolibrary.org/obo/ENVO_00002006",
            "confidence": 0.9
        },
        {
            "column_name": "AirTemperature_F",
            "concept_name": "Temperature",
            "concept_definition": "A physical quality of the thermal energy of a system.",
            "concept_id": "http://purl.obolibrary.org/obo/PATO_0000146",
            "confidence": 0.85
        },
        {
            "column_name": "WaterTemperature_F",
            "concept_name": "Water Temperature",
            "concept_definition": "The temperature of water.",
            "concept_id": "http://purl.obolibrary.org/obo/ENVO_00002010",
            "confidence": 0.95
        },
        {
            "column_name": "Lake",
            "concept_name": "Lake",
            "concept_definition": "A large body of water surrounded by land.",
            "concept_id": "http://purl.obolibrary.org/obo/ENVO_00000020",
            "confidence": 0.92
        },
        {
            "column_name": "SpeciesCode",
            "concept_name": "Taxon",
            "concept_definition": "A group of one or more populations of an organism.",
            "concept_id": "http://rs.tdwg.org/dwc/terms/Taxon",
            "confidence": 0.88
        },
        {
            "column_name": "SpeciesCode",
            "concept_name": "Scientific Name",
            "concept_definition": "The full scientific name.",
            "concept_id": "http://rs.tdwg.org/dwc/terms/scientificName",
            "confidence": 0.8
        },
    ],
    "EggMasses.csv": [
        {
            "column_name": "EggMassSubstrate",
            "concept_name": "Surface Layer",
            "concept_definition": "The layer of a material that is in contact with the surrounding medium.",
            "concept_id": "http://purl.obolibrary.org/obo/ENVO_00002005",
            "confidence": 0.7
        }
    ]
}

MOCK_GEOGRAPHICCOVERAGE_RECOMMENDATIONS = [
    {
        "id": "geo-1",
        "recommendations": [
            {
                "label": "Freshwater Lake Ecosystem",
                "uri": "http://purl.obolibrary.org/obo/ENVO_01000021",
                "ontology": "ENVO",
                "confidence": 0.75,
                "description": "An aquatic ecosystem that is part of a lake.",
                "propertyLabel": "contains",
                "propertyUri": "http://www.w3.org/ns/oa#hasBody",
            },
            {
                "label": "Temperate Climate",
                "uri": "http://purl.obolibrary.org/obo/ENVO_01000000",
                "ontology": "ENVO",
                "confidence": 0.80,
                "description": "A climate with moderate conditions",
                "propertyLabel": "contains",
                "propertyUri": "http://www.w3.org/ns/oa#hasBody",
            },
        ],
    }
]

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
      "description": "Unique ID based on date and lake surveyed",
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
  "GEOGRAPHICCOVERAGE": [
    {
      "id": "geo-1",
      "name": "Location",
      "description": "A series of small lakes within the Cedar River Municipal Watershed in the Puget Sound region of western Washington State, USA",
      "context": "Geographic Coverage"
    }
  ]
}

