import requests
import time
import psutil

# SPARQL endpoint URL
sparql_endpoint = "http://Vishnu:7200/repositories/cs/statements"

# List of SPARQL queries
sparql_queries = [
    """
    SELECT ?citations
    WHERE {
      ?document rdf:type <http://purl.org/ontology/bibo/AcademicArticle> ;
               dc:title "Summarization of Research Publications Using Automatic Extraction" ;
               amrita:Number_of_Citation ?citations .
    }
    """,
    # Add more SPARQL queries here...
]

def execute_sparql_query(query):
    start_time = time.time()
    response = requests.post(sparql_endpoint, data=query, headers={"Content-Type": "application/sparql-query;charset=utf-8"})
    execution_time = time.time() - start_time
    return response, execution_time

def measure_performance():
    for i, query in enumerate(sparql_queries, start=1):
        print(f"Executing Query {i}:")
        response, execution_time = execute_sparql_query(query)
        print("Execution Time:", execution_time, "seconds")
        
        # Measure CPU and memory usage
        cpu_usage = psutil.cpu_percent()
        memory_usage = psutil.virtual_memory().percent
        print("CPU Usage:", cpu_usage, "%")
        print("Memory Usage:", memory_usage, "%")
        
        # Print query result or error message
        if response.status_code == 200:
            print("Query Result:", response.json())
        else:
            print("Error:", response.status_code, response.text)
        print()

if __name__ == "__main__":
    measure_performance()
