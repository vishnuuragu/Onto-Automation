import requests
import pandas as pd
import os
sparql_update_endpoint = "http://Vishnu:7200/repositories/cs/statements"

folder_path = r'E:\Github Projects\Onto-Automation'
files = os.listdir(folder_path)
csv_files = [file for file in files if file.endswith('.csv')]
k=0
for csv_file in csv_files:
    df=pd.read_csv(csv_file,encoding='latin1')
    
    for i in range(len(df)):
        k=k+1
        df.at[i, 'publicationName'] = df.at[i, 'publicationName'].replace(' ', '_')  
        df.at[i, 'authors'] = df.at[i, 'authors'].replace(' ', '_')  
   
        author=[f'amrita:{x} rdf:type amrita:Author ' for x in  df["authors"][i].split(',')]
        author2=[f'amrita:hasAuthor amrita:{x}' for x in  df["authors"][i].split(',')]
         
        publicationName=df["publicationName"][i]
        description=df["description"][i]
        title=df["title"][i]
        j=str(i)
        type=df['aggregationType'][i]
        publishedDate=df["PublishedDate"][i]
        volume=df["volume"][i]
        page=df["Pages"][i]
        citation=df["citedby_count"][i]

        insert_query = f"""
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX bibo: <http://purl.org/ontology/bibo/>
        PREFIX amrita: <http://www.amrita.org/terms#>
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>
        PREFIX dc: <http://purl.org/dc/terms/>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX basic: <http://prismstandard.org/namespaces/1.2/basic/>
        INSERT DATA {{
         {'.'.join(author)} .
        amrita:{publicationName} rdf:type foaf:Organization .
        amrita:doc{k} rdf:type bibo:AcademicArticle ;
                      rdf:type bibo:{type};
        dc:publisher amrita:{publicationName} ;
        dc:issued "{publishedDate}"^^xsd:date ;
        dc:description "{description}" ;
        dc:title "{title}" ;    
        {';'.join(author2)} ;
        amrita:Number_of_Citation "{citation}"^^xsd:integer  ;
        bibo:pages "{page}"^^rdfs:Literal ;
        basic:volume "{volume}"^^rdfs:Literal .
                    
                    

            
                    
        }}
        """
        response = requests.post(sparql_update_endpoint, data={"update": insert_query})
        print(response)
        if response.status_code == 200:
            print("Data inserted successfully.")
        else:
            print(str(i) + "Error:", response.text)