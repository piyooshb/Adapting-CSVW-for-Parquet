from rdflib import Graph
from pyld import jsonld
import pandas as pd
import json
import re

"""
    Read CSVW & Parquet data file  
"""

parquet_file = r'C:\JPMC\DEV\code_repo\Test\src\local\csvw_on_parquet\input\name_and_address.parquet'
df = pd.read_parquet(parquet_file, engine='pyarrow')
# print(df)

csvw_input = 'C:\JPMC\DEV\code_repo\Test\src\local\csvw_on_parquet\input\csvw_name_and_address.json'
csvw_data = json.load(open(csvw_input))

"""
    Create Triple template from CSVW  
"""

triple_list = []

for tuples in csvw_data['tables'][0]['tableSchema']['columns']:
    if 'virtual' in tuples.keys():
        subject = tuples['aboutUrl']
        predicate = tuples['propertyUrl']
        object = tuples['valueUrl']

        triple = ('<{}> <{}> <{}> .').format(subject, predicate, object)
        triple_list.append(triple)
    else:
        subject = tuples['aboutUrl']
        predicate = tuples['propertyUrl']
        object_value = '{' + tuples['name'] + '}'
        object_datatype = tuples['datatype']

        triple = ('<{}> <{}> "{}"^^<{}> .').format(subject, predicate, object_value, object_datatype)
        triple_list.append(triple)

"""
    Create N-Triples by reading parquet dataframe and substituting using Triple template
"""

ntriples_data = []

for index, row in df.iterrows():
    for triple in triple_list:
        substitution_lst = re.findall(r'\{([^}]+)\}', triple)

        for substitution_str in substitution_lst:
            if substitution_str == '_row':
                triple = triple.replace('{_row}', '_' + str(index))
            else:
                replace_from_str = '{' + substitution_str + '}'
                replace_to_str = str(row[substitution_str])
                triple = triple.replace(replace_from_str, replace_to_str)
        ntriples_data.append(triple)

nt_output = r'C:\JPMC\DEV\code_repo\Test\src\local\csvw_on_parquet\output\name_and_address.nt'
with open(nt_output, "w") as outfile:
    outfile.write("\n".join(ntriples_data))


"""
    Serialize n-triples to JSON-LD and frame JSON-LD
"""

context = {
    "sdo": "https://schema.org/",
    "customer": "https://vocabulary.org/customer/",
    "data": "https://data.org/"
}

frame = {
    "@context": {
        "customer": "https://vocabulary.org/customer/",
        "data": "https://data.org/",
        "sdo": "https://schema.org/"
    },
    "@graph": [
        {
            "customer:hasAddress": {
                "sdo:addressLocality": {},
                "sdo:addressRegion": {},
                "sdo:postalCode": {},
                "sdo:streetAddress": {}
            },
            "customer:hasContact": {
                "sdo:email": {},
                "sdo:telephone": {}
            },
            "sdo:name": {}
        }
    ]
}

# Create a new RDF Grpah
g = Graph()

# Parse N-Triples data into the RDF Graph
for triple in ntriples_data:
    g.parse(data=triple, format="nt")

# Convert RDF Graph to JSON-LD format
json_ld = g.serialize(format="json-ld", context=context, indent=4)

from pyld import jsonld

jsonld_obj = json.loads(json_ld)
compact = jsonld.compact(jsonld_obj, context)
framed_jsonld = jsonld.frame(compact, frame)
# print(json.dumps(framed_jsonld, indent=4))

"""
    Write JSON-LD output
"""

jsonld_output = r'C:\JPMC\DEV\code_repo\Test\src\local\csvw_on_parquet\output\name_and_address.jsonld'
with open(jsonld_output, 'w') as output_file:
    output_file.write(json.dumps(framed_jsonld, indent=4))
