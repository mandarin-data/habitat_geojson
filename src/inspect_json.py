import json
import pandas as pd
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

districts = {}
for k in budapest:
    v = budapest[k]
    districts[v] = k
###############################################################################
#####              Putting stat data into the GeoJSON                     #####
###############################################################################
with open('data/merged.geojson', 'r') as f:
    hu_json = json.load(f)

for feature in hu_json['features']:
    n = hu_json['features'].index(feature)
    if 'NAME' in feature['properties']:
        name = feature['properties']['NAME']
        # either it is on our list, or it is a district
        if name in budapest.values():
            hu_json['features'][n]['properties']['NAME'] = districts[name]
            name = districts[name]
        if name in municipalities:
            # we can't call a property starting with a number in d3
            # so i put an y before each year
            hu_json['features'][n]['properties']['y2007'] = df.loc[name]['2007']
            hu_json['features'][n]['properties']['y2008'] = df.loc[name]['2008']
            hu_json['features'][n]['properties']['y2009'] = df.loc[name]['2009']
            hu_json['features'][n]['properties']['y2010'] = df.loc[name]['2010']
            hu_json['features'][n]['properties']['y2011'] = df.loc[name]['2011']
            hu_json['features'][n]['properties']['y2012'] = df.loc[name]['2012']
            hu_json['features'][n]['properties']['y2013'] = df.loc[name]['2013']
            hu_json['features'][n]['properties']['y2014'] = df.loc[name]['2014']
            hu_json['features'][n]['properties']['y2015'] = df.loc[name]['2015']
            hu_json['features'][n]['properties']['y2016'] = df.loc[name]['2016']
            hu_json['features'][n]['properties']['y2017'] = df.loc[name]['2017']

with open('data/habitat.geojson', 'w') as f:
    json.dump(hu_json, f)

with open('data/time_map.tsv.csv', 'r') as f:
    with open('data/time_corrected.tsv', 'w') as of:
        for l in f:
            l = l.strip()
            ls = l.split('\t')
            if ls[0] in budapest.keys():
                ls[0] = budapest[ls[0]]
            new_line = '\t'.join(ls) + '\n'
            of.write(new_line)
