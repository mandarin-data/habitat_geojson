import json
import pandas as pd
###############################################################################
#####                    Infor for the GeoJSON file                       #####
###############################################################################
time_map = {"type": "FeatureCollection",
            "name": "hungary",
            "crs":
                {"type": "name", "properties":
                    {"name": "urn:ogc:def:crs:OGC:1.3:CRS84"}},
            "features": []}

###############################################################################
#####          Getting place names and normalizing them                   #####
###############################################################################
df = pd.read_csv('data/time_map.tsv.csv', sep='\t', encoding='utf-8')
municipalities = list(df['NUTS5NAME'])
df.set_index('NUTS5NAME', inplace=True)

# Mapping stat names to shapefile names
budapest = {'Budapest 01. ker.': 'I. kerület',
            'Budapest 02. ker.': 'II. kerület',
            'Budapest 03. ker.': 'III. kerület',
            'Budapest 04. ker.': 'IV. kerület',
            'Budapest 05. ker.': 'V. kerület',
            'Budapest 06. ker.': 'VI. kerület',
            'Budapest 07. ker.': 'VII. kerület',
            'Budapest 08. ker.': 'VIII. kerület',
            'Budapest 09. ker.': 'IX. kerület',
            'Budapest 10. ker.': 'X. kerület',
            'Budapest 11. ker.': 'XI. kerület',
            'Budapest 12. ker.': 'XII. kerület',
            'Budapest 13. ker.': 'XIII. kerület',
            'Budapest 14. ker.': 'XIV. kerület',
            'Budapest 15. ker.': 'XV. kerület',
            'Budapest 16. ker.': 'XVI. kerület',
            'Budapest 17. ker.': 'XVII. kerület',
            'Budapest 18. ker.': 'XVIII. kerület',
            'Budapest 19. ker.': 'XIX. kerület',
            'Budapest 20. ker.': 'XX. kerület',
            'Budapest 21. ker.': 'XXI. kerület',
            'Budapest 22. ker.': 'XXII. kerület',
            'Budapest 23. ker.': 'XXIII. kerület'}

discticts = {}
for k in budapest:
    v = budapest[k]
    discticts[v] = k
###############################################################################
#####              Putting stat data into the GeoJSON                     #####
###############################################################################
with open('data/merged.geojson', 'r') as f:
    hu_json = json.load(f)

for feature in hu_json['features']:
    if 'NAME' in feature['properties']:
        # either it is on our list, or it is a district
        if feature['properties']['NAME'] in municipalities\
                or feature['properties']['NAME'] in budapest.values():
            to_add = {"type": "Feature"}
            to_add['properties'] = {}
            if feature['properties']['NAME'] in municipalities:
                name = feature['properties']['NAME']
            else:
                name = discticts[feature['properties']['NAME']]
            to_add['properties']['name'] = name
            geometry = feature['geometry']
            to_add['geometry'] = {}
            to_add['geometry']['type'] = geometry['type']
            to_add['geometry']['coordinates'] = geometry['coordinates']
            # we can't call a property starting with a number in d3
            # so i put an y before each year
            to_add['properties']['y2007'] = df.loc[name]['2007']
            to_add['properties']['y2008'] = df.loc[name]['2008']
            to_add['properties']['y2009'] = df.loc[name]['2009']
            to_add['properties']['y2010'] = df.loc[name]['2010']
            to_add['properties']['y2011'] = df.loc[name]['2011']
            to_add['properties']['y2012'] = df.loc[name]['2012']
            to_add['properties']['y2013'] = df.loc[name]['2013']
            to_add['properties']['y2014'] = df.loc[name]['2014']
            to_add['properties']['y2015'] = df.loc[name]['2015']
            to_add['properties']['y2016'] = df.loc[name]['2016']
            to_add['properties']['y2017'] = df.loc[name]['2017']
            time_map['features'].append(to_add)

with open('data/habitat.geojson', 'w') as f:
    json.dump(time_map, f)
