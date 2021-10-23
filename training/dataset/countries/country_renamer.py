"""
country_renamer.py

Reads in the HTML file and renames the countries according to their names.
"""

import json
import os

import pycountry

DIRECTORY = "."
HTML_FILE = "every-country-shape"
UNNAMED_FILE_SUFFIX = ".450.png"


id_to_name = dict()
file_to_id = dict()

with open(HTML_FILE) as f:
    for line in f:
        if 'class="photo-img" style=""' in line and 'src="/img/user-photo-library/' in line:
            id = line[line.index('data-answer="0') + len('data-answer="'):line.index('">')]
            file_name = line[line.index('-library/') + len('-library/'):line.index('" data-answer=')]
            file_name = file_name[file_name.index('/') + 1:]
            file_to_id[file_name] = id
        if line.startswith('    var _page = {"language":"english","user":null,"pageType":"photo-game","pa'):
            line = line[line.index('{"lan'):-2]
            json_rep = json.loads(line)
            
            countries = json_rep["data"]["quiz"]["answers"]
            print(str(countries)[:1000])
            for country in countries:
                id_to_name[country["id"]] = country["display"]
            break

print(file_to_id)

for entry in os.scandir(DIRECTORY):
    if entry.path.endswith("-450.png") and entry.is_file():
        processed = False
        country_name = id_to_name[file_to_id[os.path.basename(entry.path)]]
        new_name = None
        try:
            new_name = pycountry.countries.get(name=country_name).alpha_3
            processed = True
        except AttributeError:
            try:
                new_name = pycountry.countries.search_fuzzy(country_name)[0].alpha_3
                processed = True
            except:
                print(f"Could not process '{str(entry.path)}' to '{country_name}'")
        if processed:
            new_name = new_name.lower() + ".png"
            print(f"Renamed '{str(entry.path)}' to '{country_name}' to '{new_name}'.")
            os.rename(entry.path, new_name)
