from mind_mapper import app

@app.route('/', methods=['GET'])
def home():
    return 'Hello, World!'
