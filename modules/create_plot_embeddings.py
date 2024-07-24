from langchain.vectorstores import Neo4jVector
from langchain_community.vectorstores import Neo4jVector
from langchain_openai import OpenAIEmbeddings
import os
from graphdatascience import GraphDataScience
import time
from dotenv import load_dotenv

load_dotenv()


database = os.getenv('NEO4J_DATABASE')
uri, user, password = os.getenv('NEO4J_URI'), os.getenv('NEO4J_USER'), os.getenv('NEO4J_PASSWORD')
gds = GraphDataScience(
    uri,
    auth = (user, password), database=database
)        

def create_plot_embeddings():
    try:
        gds.run_cypher("DROP INDEX overview_embeddings2 IF EXISTS")
        print("Index dropped")
    except:
        print("No index to drop")
        
    del_embedding = """CALL apoc.periodic.iterate(
    "MATCH (n:Movie) RETURN n",
    "SET n.embedding = NULL", 
    {batchSize: 100}
    );
    """
    gds.run_cypher(del_embedding)

    print("Creating index")
    start = time.time()

    query_index = (
                "CREATE VECTOR INDEX overview_embeddings2 "
                "FOR (m: Movie) ON (m.embedding) "
                "OPTIONS {indexConfig: { "
                "`vector.dimensions`: 1536, "
                "`vector.similarity_function`: 'cosine'}}"
            )            
            
    gds.run_cypher(query_index)   

    Neo4jVector.from_existing_graph(
        embedding= OpenAIEmbeddings(), 
        url=os.getenv('NEO4J_URI'), 
        username=os.getenv('NEO4J_USER'), 
        password=os.getenv('NEO4J_PASSWORD'),
        index_name='overview_embeddings2',
        node_label="Movie",
        text_node_properties=['overview','keyword','collection'],
        embedding_node_property='embedding',
        search_type = 'VECTOR'
    )

    end = time.time()
    print("Index created")
    print("Elapsed Time : ", end - start)