# %%
import os
import json
import ast
import pytz
import requests
from datetime import datetime
from urllib.parse import urlparse

# from pydatajson import DataJson
# from pydatajson.writers import write_xlsx_catalog

SITE_URL = "https://datosabiertos.desarrollosocial.gob.ar"
QUERY_URL = 'http://10.80.5.13:5000/'

BASE_DICT = {
    "version": "1.1",
    "identifier": "desarrollo-social",
    "title": "Datos abiertos del Ministerio de Desarrollo Social",
    "description": "Ponemos a tu alcance datos públicos del Ministerio de Desarrollo Social de la Nación en formatos abiertos de modo que puedas usarlos y compartirlos. Te proponemos, a través de este portal, tener un punto de encuentro entre el ministerio, las organizaciones de la sociedad civil y los ciudadanos.",
    "superThemeTaxonomy": "http://datos.gob.ar/superThemeTaxonomy.json",
    "publisher": {
        "mbox": "datosabiertos@desarrollosocial.gob.ar",
        "name": "Ministerio de Desarrollo Social de la Nación",
    },
    "issued": "",
    "modified": f'{datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")}',
    "language": ["spa"],
    "license": "cc-nc",
    "homepage": "https://datosabiertos.desarrollosocial.gob.ar/",
    "rights": "",
    "spatial": ["ARG"],
    "themeTaxonomy": [],
}


def gen_datasetinfo(dataset_id):
    dataset_url = f"{QUERY_URL}/api/3/action/package_show?id={dataset_id}"
    r = requests.get(dataset_url)
    dataset_info = r.json()["result"]
    dataset = {
        "title": dataset_info["title"],
        "description": dataset_info["notes"],
        "modified": dataset_info["metadata_modified"],
        "identifier": dataset_info["id"],
        "issued": dataset_info["metadata_created"],
        "landingPage": dataset_info["url"],
        "license": dataset_info["license_title"],
        "spatial": ["ARG"],
        "publisher": {
            "mbox": dataset_info["author_email"],
            "name": dataset_info["author"],
        },
        "contactPoint": {
            "fn": dataset_info["maintainer"],
            "hasEmail": dataset_info["maintainer_email"],
        },
        "distribution": gen_resources(dataset_info),
        "keyword": list(tag["name"] for tag in dataset_info["tags"]),
        "superTheme": dataset_info["super_theme"]
        .replace("{", "")
        .replace("}", "")
        .split(","),
        "accrualPeriodicity": dataset_info["update_frequency"],
        "language": ["spa"],
    }
    return dataset


def gen_resources(dataset_info):
    resources = dataset_info["resources"]
    datasets = []
    for r in resources:
        try:
            fields = ast.literal_eval(r["file_fields_dict"])
        except:
            fields = []

        datasets.append(
            {
                "identifier": r["id"],
                "format": r["format"],
                "title": r["name"],
                "description": r["description"],
                "type": "file.upload",
                "issued": r["created"],
                "modified": r["last_modified"],
                "license": "cc-by",
                "accessURL": f"{SITE_URL}/dataset/{dataset_info['id']}/resource/{r['id']}",
                "field": fields,
                "downloadURL": r["url"],
                "fileName": os.path.basename(urlparse(r["url"]).path),
            }
        )

    return datasets


def latest_update():
    response = requests.get(f"{QUERY_URL}/data.json")
    data = response.json()
    return max([x["modified"] for x in data["dataset"]])

if __name__ == "__main__":
    datasets_url = f"{QUERY_URL}/api/3/action/package_list"
    r = requests.get(datasets_url)
    datasets_id = r.json()["result"]
    
    datasets = []
    for d in datasets_id:
        datasets.append(gen_datasetinfo(d))
    
    BASE_DICT["dataset"] = datasets
    
    if max([x["modified"] for x in BASE_DICT["dataset"]]) > latest_update():
        with open(
            f"{os.path.abspath(os.path.dirname(__file__))}/public/data.json", "w"
        ) as outfile:
            json.dump(BASE_DICT, outfile, indent=4)
