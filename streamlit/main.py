import streamlit as st
import pickle
import pandas as pd

# python -m streamlit run main.py
st.title('Legendary Pokemon Predictor')
st.caption("Predict whether a Pokémon is Legendary based on its base stats.")

model = pickle.load(open('../models/production.sav', 'rb'))

name = st.text_input("Pokémon Name")

hp = st.number_input("HP", min_value=1, max_value=255)
attack = st.number_input("Attack", min_value=1, max_value=255)
defense = st.number_input("Defense", min_value=1, max_value=255)
sp_attack = st.number_input("Special Attack", min_value=1, max_value=255)
sp_defense = st.number_input("Special Defense", min_value=1, max_value=255)
speed = st.number_input("Speed", min_value=1, max_value=255)


TYPES = ["Normal", "Fire", "Water", "Grass", "Bug", "Electric", "Rock", "Psychic", "Dark", "Dragon", "Fighting", "Ghost", "Poison", "Ground", "Steel", "Ice", "Fairy", "Flying"]
type1 = st.selectbox("Primary Type", TYPES)
type2 = st.selectbox("Secondary Type", ["None"] + TYPES)
generation = st.number_input("Generation", min_value=1, max_value=9)

if st.button("Predict"):
    total = hp + attack + defense + sp_attack + sp_defense + speed
    pokemon = pd.DataFrame({
        "name": [name],
        "type1": [type1],
        "type2": [type2 if type2 != "None" else ""],
        "hp": [hp],
        "attack": [attack],
        "defense": [defense],
        "sp_attack": [sp_attack],
        "sp_defense": [sp_defense],
        "speed": [speed],
        "total": [total],
        "generation": [generation]
    })

    prediction = model.predict(pokemon)[0]
    probability = model.predict_proba(pokemon)[0][1]

    label = "🌟 Legendary" if prediction else "🔵 Not Legendary"
    pokemon_label = f"**{name}**" if name.strip() else "This Pokémon"
    st.subheader(f"{pokemon_label} is: {label}")
    st.write(f"Probability of being Legendary: {probability*100:.2f} %")
