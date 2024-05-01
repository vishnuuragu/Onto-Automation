import requests
import time
import psutil

# SPARQL endpoint URL
sparql_endpoint = "http://Vishnu:7200/repositories/cs"

# List of SPARQL queries
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
    # Add more SPARQL queries here...
]

def execute_sparql_query(query):
    start_time = time.time()
    cpu_before = psutil.cpu_percent()
    memory_before = psutil.virtual_memory().percent
    
    response = requests.post(sparql_endpoint, data={"query": query})
    
    execution_time = time.time() - start_time
    cpu_after = psutil.cpu_percent()
    memory_after = psutil.virtual_memory().percent
    
    cpu_usage = cpu_after - cpu_before
    memory_usage = memory_after - memory_before
    
    return response, execution_time, cpu_usage, memory_usage

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
        try:
            result = response.json()
            print("Query Result:", result)
        except ValueError as e:
            print("Error decoding JSON response:", e)
            print("Response text:", response.text)
        
        print()


if __name__ == "__main__":
    measure_performance()
