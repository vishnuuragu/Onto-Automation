import requests
import time
import psutil

sparql_endpoint = "http://Vishnu:7200/repositories/cs"

sparql_queries = [
    """
    PREFIX bibo: <http://purl.org/ontology/bibo/>
    PREFIX dc: <http://purl.org/dc/terms/>
    PREFIX amrita: <http://www.amrita.org/terms#>

    SELECT ?citations
    WHERE {
      ?document rdf:type bibo:AcademicArticle ;
               dc:title "Summarization of Research Publications Using Automatic Extraction" ;
               amrita:Number_of_Citation ?citations .
    }
    """,
    """
    PREFIX bibo: <http://purl.org/ontology/bibo/>

    SELECT (COUNT(?conferencePaper) AS ?count)
    WHERE {
      ?conferencePaper rdf:type bibo:Conference .
    }
    """,
    """
    PREFIX bibo: <http://purl.org/ontology/bibo/>
    PREFIX dc: <http://purl.org/dc/terms/>

    SELECT ?publisher
    WHERE {
      ?article rdf:type bibo:AcademicArticle ;
               dc:title "Personalized Abstract Review Summarization Using Personalized Key Information-Guided Network" ;
               dc:publisher ?publisher .
    }
    """,
    """
    PREFIX bibo: <http://purl.org/ontology/bibo/>
    PREFIX dc: <http://purl.org/dc/terms/>
    PREFIX amrita: <http://www.amrita.org/terms#>

    SELECT ?Author
    WHERE {
      ?article rdf:type bibo:AcademicArticle ;
               dc:title "Personalized Abstract Review Summarization Using Personalized Key Information-Guided Network" ;
               amrita:hasAuthor  ?Author .
    }
    """,
    """
    PREFIX bibo: <http://purl.org/ontology/bibo/>
    PREFIX amrita: <http://www.amrita.org/terms#>

    SELECT (COUNT(?article) AS ?count)
    WHERE {
      ?article rdf:type bibo:AcademicArticle ;
               amrita:hasAuthor amrita:Gowtham_Ramesh .
    }
    """,
    """
    PREFIX amrita: <http://www.amrita.org/terms#>

    SELECT ?article ?citationCount
    WHERE {
      ?article amrita:Number_of_Citation ?citationCount .
      FILTER (?citationCount > 20)
    }
    """
]

def execute_sparql_query(query):
    start_time = time.time()
    response = requests.post(sparql_endpoint, data={"query": query})
    execution_time = time.time() - start_time
    return response, execution_time


def measure_performance():
    total_execution_time = 0
    for i, query in enumerate(sparql_queries, start=1):
        print(f"Executing Query {i}:")
        response, execution_time = execute_sparql_query(query)
        print("Execution Time:", execution_time, "seconds")
        total_execution_time += execution_time
        
        # Print query result or error message
        try:
            result = response.json()
            if isinstance(result, dict) and 'results' in result:
                # Handle SPARQL JSON results
                print("Query Result:", result['results']['bindings'])
            else:
                # Handle non-JSON results
                print("Query Result:", result)
        except ValueError as e:
            # print("Error decoding JSON response:", e)
            print("Response text:", response.text)
        
        print()
    
    print("Total Execution Time for all queries:", total_execution_time, "seconds")

if __name__ == "__main__":
    measure_performance()
