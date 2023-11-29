from flask import Flask, jsonify, abort, request
import json

json_file = "animations.json"

with open(json_file, "r") as file:
    data = json.load(file)

app = Flask(__name__)

@app.route('/')
def index():
    return "Welcome to Main Page!"

@app.route('/titles')
def showtitles():
    movie_list = data["animations"]
    movie_titles = []

    for i in movie_list:
        movie_titles.append(i["Original title"])

    return jsonify(movie_titles)

@app.route('/ids/<int:id>')
def showdetails(id):
    animation = next((anim for anim in data.get('animations', []) if anim.get('ID') == id), None)

    details = {
        "ID": animation.get('ID'),
        "Original Title": animation.get('Original title'),
        "Studio": animation.get('Studio'),
        "Year of Production": animation.get('Year of production'),
        "Time": animation.get('Time'),
        "Directors": animation.get('Directors'),
        "Keywords": animation.get('Keywords')
    } if animation else abort(404)

    return details

@app.route('/titles/<string:keyword>')
def searchby(keyword):
    inverted_index = {}
    for animation in data.get('animations', []):
        animation_id = animation.get('ID')
        keywords = animation.get('Keywords', [])
        for kw in keywords:
            inverted_index.setdefault(kw.lower(), []).append(animation_id)

   
    keyword_lower = keyword.lower()

    matching_animation_ids = inverted_index.get(keyword_lower, [])

    if matching_animation_ids:
        matching_animation_titles = [
            animation.get('Original title') for animation in data.get('animations', []) if animation.get('ID') in matching_animation_ids
        ]
        return matching_animation_titles
    else:
        abort(404)

@app.route('/studios/<int:id>', methods=['PUT'])
def setstudio(id):

    new_studio_name = request.args.get('studio')

    if not new_studio_name:
        abort(400, "Brak parametru: Studio")

    animation_details = update_studio_by_id(id, new_studio_name)

    if animation_details:
        return jsonify({
            "message": f"Nazwa Studio dla bajki o ID {id} zaaktualizowane do '{new_studio_name}'",
            "animation_details": animation_details
        }), 200
    else:
        abort(404)

def update_studio_by_id(animation_id, new_studio_name):

    animation = next((anim for anim in data.get('animations', []) if anim.get('ID') == animation_id), None)

    if animation:
        animation['Studio'] = new_studio_name

        with open(json_file, 'w') as write_file:
            json.dump(data, write_file, indent=2)

        return {
            "ID": animation.get('ID'),
            "Original Title": animation.get('Original title'),
            "Studio": animation.get('Studio'),
            "Year of Production": animation.get('Year of production'),
            "Time": animation.get('Time'),
            "Directors": animation.get('Directors'),
            "Keywords": animation.get('Keywords')
        }
    else:
        return None

if __name__ == "__main__":
    app.run(debug=True)