from langchain_ollama import OllamaLLM
import pandas as pd
import itertools
def generate_ol(data):
    #turn data in to lists and join together in one big string with a known divider : 
    li = data.values.tolist()
    flat_li = itertools.chain(li)
    #print(flat_li)
    data_str = "|".join(map(str, flat_li))
    #print(data_str)
    #join to one big string 
    model = OllamaLLM(model="llama3")
    inputs = (
        "You are an assistant for Pokémon data questions. "
        "Please provide two to three comments on the given data. "
        "The Data covers Pokemons: Grade i.e. the quality of the card, Avg. Actual Price which is the averages of the prices sold for that grade, Forecasted Price which is the forecasted price so marked grade. "
        "DO NOT the reader for more context, clarification, or elaboration and DO NOT repeat Anything from this prompt. "
        "The data is divided into individual observations using '|':\n"
        f"Data: {data_str}\n\nAnswer: "
    )
    #get answer
    results = model.invoke(inputs)
    return results