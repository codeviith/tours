from flask import Flask, make_response, jsonify, request, g
import json

app = Flask(__name__)

@app.before_request
def load_data():
    with open("db.json") as f:
        g.data: dict = json.load(f)

@app.after_request
def save_data(response):
    with open('db.json', 'w') as f:
        json.dump(g.data, f, indent=4)
    return response

@app.route("/")
def root():
    return "<h1>Welcome to the simple json server</h1>"

#@app.route('/langs', methods=['GET','POST'])
@app.get("/langs")
def get_langs():
    data = g.data['langs']
    return make_response(jsonify(data), 200)

@app.get("/langs/<int:id>")
def get_lang_by_id(id: int):
    lang_list = g.data['langs']
    for lang in lang_list:
        if lang['id'] == id:
            return make_response(jsonify(lang), 200)
    return make_response(jsonify({"Error":"Language not found"}, 404))



# TODO: write post route
@app.post('/lang')
def post_lang():
    request_data = request.json
    max_id = 0
    for lang in g.data['langs']:
        if lang['id'] >  max_id:
            max_id = lang['id']
    assert max_id != 0, "Max ID not found"
    
    max_id = max([lang['id'] for lang in g.data['langs']])
    request_data['id'] = max_id + 1
    print(type(g.data['langs']))
    g.data['langs'].append(request_data)
    return make_response(jsonify(request_data), 201)

# TODO: write delete route
@app.delete('/langs')
def delete_lang(id):
    new_lang_list = []
    for lang in g.data['langs']:
        if lang['id'] != id:
            new_lang_list.append(lang)
    g.data['langs'] = [lang for lang in g.data['langs'] if lang['id'] != id]

    assert lang['id'] != id, "ID not found"

    return make_response(jsonify({}), 200)


# TODO: write patch route  ##### skip for now...#####
# @app.patch('/langs')
# def patch_lang(id):
#     request_data = request.json
#     for lang in g.data['langs']:
#         if lang['id'] == id:
#             pass
#     return ""


if __name__ == "__main__":
    app.run(port=5555, debug=True)


