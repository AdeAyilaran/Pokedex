"""
Create a Flask application that allows users to interact with a set of data, either stored in a .csv
file or from a web-based API.
"""

# Import statements
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from flask import Flask, redirect, url_for, render_template, request, session, flash

# This is some housekeeping so that Pycharm prints out all of the columns
desired_width = 320
pd.set_option('display.width', desired_width)
np.set_printoptions(linewidth = desired_width)
pd.set_option('display.max_columns', 20)

# Flask housekeeping
app = Flask(__name__)

# Reading the .csv file
pokemon = pd.read_csv("databases/pokedex_basic.csv", delimiter = ',')

@app.route("/")
def home_page():
    return render_template("homepage.html", title = 'Pokemon Table', pokemon = pokemon)

@app.route("/view_pokemon/<name>", methods = ["GET", "POST"])
def view_pokemon(name):
    if request.method == "GET":
        for index, row in pokemon.iterrows():
            if name == row['Name']:
                return render_template("view_pokemon.html", content = row)
    else:
        return redirect(url_for("delete_pokemon"))


@app.route("/add_pokemon", methods = ["GET", "POST"])
def add_pokemon():
    types = ['Water', 'Grass', 'Fire', 'Bug', 'Flying', 'Rock', 'Ground', 'Fighting', 'Psychic', 'Ghost', 'Steel', 'Ice', 'Dragon', 'Normal', 'Dark', 'Fairy']
    if request.method == "POST":
        new_row = {"PokedexNumber": request.form["pnumber"], "Name": request.form["pname"],
                   "Type": (request.form["ptype1"]+request.form["ptype2"]) , "Total": request.form["ptotal"],
                   "HP": request.form["php"], "Attack": request.form["pattack"], "Defense": request.form["pdefense"],
                   "SpecialAttack": request.form["pspattack"], "SpecialDefense": request.form["pspdefense"],
                   "Speed": request.form["pspeed"]}

        global pokemon

        pokemon = pokemon.append(new_row, ignore_index=True)
        return redirect(url_for("home_page"))
    else:
        return render_template("add_pokemon.html", types = types)

@app.route("/delete_pokemon", methods = ["GET", "POST", "DELETE"])
def delete_pokemon():
    global pokemon

    pokemon_id = request.args.get('pokemon_id')
    index_to_delete = pokemon.index[pokemon['Name'] == pokemon_id].tolist()
    pokemon = pokemon.drop(index_to_delete)
    # pokemon_to_delete = pokemon[pokemon['Name'] == pokemon_id]
    return redirect(url_for("home_page"))

if __name__ == "__main__":
    app.run(debug = True)
