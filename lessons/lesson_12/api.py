

app = Flask(__name__)


class Model:

    def __init__(self, obj={}):
        """@param obj {dict}"""
        self._obj = obj

    def get_obj(self):
        return self._obj

    def set_property(self, name, value):
        self._obj[name] = value

    def set_properties(self, properties):
        """@param properties {dict}"""
        self._obj.update(properties)

    def delete_property(self, name):
        if name in self._obj:
            del self._obj[name]

    @staticmethod
    def serialize(model):
        return json.dumps(model._obj, sort_keys=True, indent=4)

    @staticmethod
    def deserialize(string):
        return Model(json.loads(string))



@app.route('/', methods=['GET'])
def hello():
    return 'hello:)'


@app.route('/api/<key>', methods=['GET'])
def get(key):
    model = get_model(key)
    if model is None:
        return "NOT FOUND"
    else:
        return jsonify(model.get_obj())


@app.route('/api/<key>', methods=['POST'])
def post(key):
    result = set_property(key, json.loads(request.data))
    return jsonify(result.get_obj())


@app.route('/api/<key>/<property_name>', methods=['DELETE'])
def delete(key, property_name):
    result = delete_property(key, property_name)
    if result is None:
        return "NOT FOUND"
    else:
        return jsonify(result.get_obj())



def get_model(key):
    return read_model(key)


def set_property(key, properties):
    data = read_model(key)
    if data is None:
        data = Model()
    data.set_properties(properties)
    result = write_model(key, data)
    return result


def delete_property(key, property_name):
    data = read_model(key)
    if data is None:
        return None
    if property_name not in data.get_obj():
        return None
    data.delete_property(property_name)
    result = write_model(key, data)
    return result



def read_model(key):
    file_name = key + '.json'
    try:
        with open(file_name, 'r') as f:
            return Model.deserialize(f.read())
    except IOError as e:
        print (e)
        return None


def write_model(key, model):
    file_name = key + '.json'
    try:
        with open(file_name, 'w') as f:
            f.write(Model.serialize(model))
            return model
    except IOError as e:
        print (e)
        return None


if __name__ == '__main__':
    app.run(debug=True)