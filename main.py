import os
import requests
import json
import random

NOTION_BEARER_TOKEN = os.environ.get("NOTION_BEARER_TOKEN")
DATABASE_ID = "01f5145b31654dcbb56b7c7d9c20bea4"

_headers = {
    "Authorization": f"Bearer {NOTION_BEARER_TOKEN}",
    "Notion-Version": "2022-06-28",
}

TARGET_LIST = [
    "Responsible",
    "Accountable",
    "Consulted",
    "Informed",
]


def get_db_data():
    response = requests.get(
        f'https://api.notion.com/v1/databases/{DATABASE_ID}',
        headers=_headers
    )
    return response.json()

def update_db_properties(payload):
    response = requests.patch(
        f'https://api.notion.com/v1/databases/{DATABASE_ID}',
        headers=_headers,
        json=payload
    )
    return response.json()


def get_all_properties_values():
    data = get_db_data()
    properties = data['properties']

    values = set()
    colors = set()

    for t in TARGET_LIST:
        options = properties[t]['multi_select']['options']
        for x in options:
            values.add(x['name'])
            colors.add(x['color'])

    values_list = sorted(values)
    return [
        {
            "name": i,
            "color": random.choice(sorted(colors)),
        }
        for i in values_list

    ]


def standardize_property_values():
    options = [
        {
            "name": "ALL",
            "color": "purple"
        },
        {
            "name": "Allan",
            "color": "red"
        },
        {
            "name": "Brendan",
            "color": "brown"
        },
        {
            "name": "CX",
            "color": "purple"
        },
        {
            "name": "Corporate",
            "color": "pink"
        },
        {
            "name": "DATA",
            "color": "purple"
        },
        {
            "name": "Dave",
            "color": "default"
        },
        {
            "name": "ELT",
            "color": "orange"
        },
        {
            "name": "ENG",
            "color": "blue"
        },
        {
            "name": "GTM",
            "color": "green"
        },
        {
            "name": "Grace",
            "color": "purple"
        },
        {
            "name": "Jason",
            "color": "gray"
        },
        {
            "name": "Keith",
            "color": "blue"
        },
        {
            "name": "Noah",
            "color": "red"
        },
        {
            "name": "PDE",
            "color": "green"
        },
        {
            "name": "Product",
            "color": "brown"
        },
        {
            "name": "REV OPS",
            "color": "pink"
        },
        {
            "name": "Sangeetha",
            "color": "default"
        },
        {
            "name": "Sebastian",
            "color": "green"
        },
        {
            "name": "Steve",
            "color": "yellow"
        },
        {
            "name": "Taylor",
            "color": "gray"
        },
        {
            "name": "Wake",
            "color": "red"
        },
        {
            "name": "Whitney",
            "color": "purple"
        }
    ]
    null_out_payload = {
        "properties": {
            i: {
                "multi_select":
                    {
                        'options': []

                    }

            }
            for i in TARGET_LIST
        }
    }
    payload = {
        "properties": {
            i: {
                "multi_select":
                    {
                        'options': options

                    }

            }
            for i in TARGET_LIST
        }
    }
    # needs to null out the previous in order to standardize
    update_db_properties(null_out_payload)
    return update_db_properties(payload)


if __name__ == '__main__':
    print(json.dumps(standardize_property_values()))
