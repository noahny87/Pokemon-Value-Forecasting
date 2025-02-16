#get pokemon card data from price charting
#put final notebook code here to run as simple script
import pandas as pd
import re
import difflib as dfl
import requests as req
import os 
# Function to load PokemonCard data
def load_pokemon_cards(file_path):
    return pd.read_excel(file_path)

# Function to read HTML data from the URL
def read_html_data(url):
    return pd.read_html(req.get(url, headers={'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'}).text)

# Function to extract grades from titles
def extract_grade_from_title(title, grades):
    title = str(title)
    i = 0
    for grade in grades:
        index = title.find(f" {grade} ")#find the grade
        if index != -1:
            return grade
    return None

# Function to clean and process auction data
def process_auction_data(auction_data, grades):
    card_data = pd.DataFrame()
    for i in auction_data[1:]:  # Iterate through each dataframe in P2 starting from index 1
        if i.shape[0] > 1 and i.shape[1] > 2:  # Only proceed if there are more than 1 row
            i = pd.DataFrame(i)  # Ensure that i is a DataFrame
            title = i.iloc[0, 2]
            
            found_grade = extract_grade_from_title(title, grades)
            
            if found_grade:
                grade_key = f"Grade_{found_grade}"
                i[grade_key] = found_grade
                card_data = pd.concat([card_data, i])
    return card_data

# Function to clean the CardData dataframe
def clean_card_data(card_data):
    card_data.drop(card_data.columns[4], axis=1, inplace=True)
    card_data.drop("TW", axis=1, inplace=True)
    
    # Adjust remaining column names
    cols = card_data.columns
    card_data.rename(columns={cols[1]: "Title", cols[2]: "Price", cols[0]: "Date Sold"}, errors="ignore", inplace=True)
    
    card_data.fillna(0, inplace=True)
    
    # Convert grades to numeric
    card_data[cols[3:]] = card_data[cols[3:]].apply(pd.to_numeric, errors="coerce")
    
    # Combine grades into one column
    card_data["Grade"] = card_data[cols[3:]].sum(axis=1)
    
    # Remove extra columns
    card_data = pd.concat([card_data.iloc[:, :3], card_data.iloc[:, -1]], axis=1)
    #format price column 
    card_data['Price'] = card_data['Price'].str.replace("$","")
    card_data['Price'] = card_data['Price'].str.replace(",","")
    card_data['Price'] = card_data['Price'].astype(float)
    return card_data

# Main function to execute the script
def main(url):
    # Read HTML auction data
  
    auction_data = read_html_data(url)
    #get card name from url
    card_name = re.search(r'(.*?)/', url[::-1]).group(1)
    card_name = card_name[::-1]
    #clean name 
    card_name = re.sub('[\W_]+', ' ', card_name)
    
    # Define the possible grades
    grades = ["1", "2", "3", "4", "5", "6", "7", "7.5", "8", "9", "9.5", "10"]
    
    # Process the auction data
    card_data = process_auction_data(auction_data, grades)
    # Add data to the PokemonCards dataframe and makesure all instances are unique
    # Clean the card data
    card_data = clean_card_data(card_data)
    #append names to card data
    card_data['name'] = card_name 
    
    print("Data has been created successfully!")
    return card_data
# may not need database search function for pokemon as each url may not work the same due to their change so making an input url function by directing to price charting could work
# Call the main function to run the script\

if __name__ == "__main__":
    main()
