
import pandas as pd 
import streamlit as st
import model, WebData, URL,chat
import time

st.title("Pokémon Card Value Forecasting🐉📈💵")
st.write(
    "### Welcome to the Pokémon Card Value Forecasting App! 🎴📈\n\n"
    "This app uses a **Random Forest forecasting model** to analyze Pokémon card prices, helping you make more informed buying and selling decisions.\n\n"
    
    "**How It Works:**\n"
    "The data is dynamically scraped from **PriceCharting** (my personal favorite), pulling the **30 most recent eBay sales** for each grade. "
    "This provides quick and efficient updates, but keep in mind that the small sample size may emphasize currently 'hot' cards rather than long-term trends.\n\n"

    "**Key Considerations:**\n"
    "- **Time Sensitivity:** Only certain high-value cards (typically **$100–$200+** in raw, ungraded condition) see significant time-based price trends.\n"
    "- **Grading Impact:** **PSA/BGS grades** heavily influence prices across all cards—sometimes even more than time.\n"
    "- **Haggling Factor:** Whether online or at card shows, final prices often come down to negotiation, especially for high-value cards.\n\n"

    "**Use Case:**\n"
    "This tool provides a **quick, rough estimate** of a card’s value based on recent market data. While it doesn’t currently factor in long-term price trends, "
    "it can still be a useful reference when buying, selling, or trading.\n\n"

    "**Important Note:**\n"
    "For best results, be as specific as possible when entering a card name! For example, searching **'Charizard'** might return vastly different results "
    "than **'First Edition Base Set Charizard 4/102'**.\n\n"

    "Happy Trading & Good Luck! 🎉"
)

st.spinner("Generating Analysis...")
pokemon_card  = st.text_input(" :green[Enter Specific Pokemon Card!]")
#pokemon_card = "Suicune gold star 115"
#run pokemon card through webscrape and prediction analysis
if pokemon_card:
#get url
    url = URL.geturl(pokemon_card)
#get data
    data = WebData.main(url)
#forecast 
    Fcast_data = model.main(data)
#show data frame 
    st.dataframe(Fcast_data)
#plot a chart
    st.scatter_chart(Fcast_data, x = "Grade",y = ["Avg. Actual Price","Forecasted Price"])
#add Ollama capability to print table output
    chat_out = chat.generate_ol(Fcast_data)
    time.sleep(5)
    chat_out
