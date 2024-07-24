from modules.relationship import getRelationship
import os
from graphdatascience import GraphDataScience
from langchain_core.tools import tool
from pydantic.v1 import BaseModel, Field
from dotenv import load_dotenv
load_dotenv()


        
database = 'movies.main'    

# uri, user, password = read_params_from_file(wd+"\\params.txt") 
uri, user, password = os.getenv('NEO4J_URI'), os.getenv('NEO4J_USER'), os.getenv('NEO4J_PASSWORD')
gds = GraphDataScience(
    uri,
    auth = (user, password), database=database
)       
class SearchInput(BaseModel):
    question: str = Field(...,description="The question asked by the user related to either the plot or genre of the movie. It essentially would not have enties or names, but just a general statement or question about the movie's plot")
        
@tool(args_schema=SearchInput)
def vectorSearch(question: str) -> list:
    """
    Find movies based on the plot or genre of the movie using vector search on the question asked by the user on the plot or genre of the movie.
    """
    
    relationship = getRelationship(question)
    params={"openAiApiKey":os.getenv('OPENAI_API_KEY'),
            "openAiEndpoint": 'https://api.openai.com/v1/embeddings',
            "question": question,
            "top_k": 10}
    query = """
        WITH genai.vector.encode(
            $question, 
            "OpenAI", 
            {
              token: $openAiApiKey,
              endpoint: $openAiEndpoint
            }) AS question_embedding
        CALL db.index.vector.queryNodes(
            'overview_embeddings2', 
            $top_k, 
            question_embedding
        ) YIELD node AS movie, score
        WHERE movie.name IS NOT NULL """ + relationship + """
        RETURN movie.name, movie.overview, score
        """
    
    # print(query)
    df = gds.run_cypher(query, 
        params = params)
    
    x_list = df['movie.name'].head().tolist()
    
    y_list = df['movie.overview'].head().tolist()
    
    combined_list = [x + ' : ' + y for x, y in zip(x_list, y_list)]

    return combined_list
    