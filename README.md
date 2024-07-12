# Usage

The process aims to leverage CSV on the Web (CSVW) to specify enriched metadata for Parquet dataset and enable mapping to Linked Data formats. The process is detailed as follows:

- Read CSVW & Parquet data files
- Extract Triplets from CSVW to generate Linked Data Template
- Parse data from Parquet file over Linked Data Template to generate N-Triples file
- Convert N-Triples data to JSON-LD document

   *Input Files:*    
   **csvw_name_and_address.json** : CSVW designed for Name & Address Parquet dataset \
   **name_and_address.parquet** : Name & Address dataset stored in Parquet file format

   *Output Files:* \
   **name_and_address.nt** : Modernized searialized Avro \
   **name_and_address.jsonld** : Modernized searialized Avro
    
   *Note*: We were not able to upload *name_and_address.parquet* to the Github Repo due to a file upload error. However, the parquet data file can be reproduced by parsing CSV data **name_and_address.csv** and writing to a Parquet File using `python csv_to_parquet.py` 
   
    `python CSVW_for_Parquet.py`


# Documentation

**Dependencies**
- Python >= 3.8

**Python Libraries**

  - json
  - pyld
  - rdflib
  - pandas
  - re
  - os

# Purpose

> Apache Parquet is an open source, column-oriented data format designed for efficient data storage and retrieval. It is designed to handle complex data in bulk and is one of the most efficient storage options in the current big data ecosystem. It provides multiple benefits - both in terms of memory consumption and fast query processing making it the most favored data format for many of today's data storage and processing services.
> 
> Parquet file contains basic metadata including schema and structure that ensures data stored in a Parquet file conforms to predefined schema within the scope of that individual Parquet file. However, vocabulary and open standards cannot be applied to this basic metadata, and it is not possible to use common vocabulary to represent the same information across more than one Parquet file. This limitation restricts seamless integration of semantic information across multiple Parquet datasets. Hence, we need an enriched metadata which supports Open standards for Parquet. Moreover, we can leverage such enriched metadata as a mapping mechanism to convert Parquet data into Linked Data formats, allowing on-demand creation of linked datasets for advanced analytics.
> 
> CSVW (CSV on the Web) is one such standard developed by W3C (World Wide Web Consortium) to describe the contents and structure of CSV data on the web. CSVW provides a metadata vocabulary that allows publishers to express the tabular structure of CSV data and includes recommendations for transforming CSV files into various Linked Data formats. 
>
> As both CSV and Parquet support tabular data, it is possible to define a specification based on CSVW for Parquet files. Our approach leverages CSVW to enrich metadata, enhance schema, apply standard vocabulary, and overlay linked structure which is used to map Parquet data to Linked Data formats such as RDF, JSON-LD, N-Triples etc.
> 
> We utilize the vocabulary, metadata, and linked structures in the CSVW to build a “Linked Data Template” which is then referenced for processing Parquet files to build relationships within the dataset. The Parquet data is transformed to generate a list of triples where each triple represents a set of subject, predicate and object. These triples are a line-based, plain text serialization for RDF (Resource Description Framework) and stored in Linked Data format such as N-Triples.
> 
> Thus, by publishing CSVW with Parquet files, modern data concepts such as interoperability, data sharing and data reuse can be applied to Parquet files. The ability to convert Parquet data into Linked Data formats also enables quick conversion into graph for semantic search as well as advanced AI (Artificial Intelligence) & Data Science applications such as Neural Networks and Large Language Models (LLMs).

