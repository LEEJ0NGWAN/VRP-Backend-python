from flask import Blueprint, Response, request, jsonify
from serialize import serialize
from error_handler import Error, register_handler
from downloader import downloads
from sift import init, work
from thread import Thread

app = Blueprint('s3_api', __name__)
register_handler(app)

@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({})

@app.route('/match', methods=['POST'])
def featureMatching():
    data = request.get_json(silent=True)
    print(data)
    if 'sceneFileLocation' not in data\
    or 'evidenceFileLocations' not in data:
        raise Error(status_code=400)

    # for key in data:
    #     downloads(data[key])

    Thread(target=init, args=(data['evidenceFileLocations'], ))

    # for key in data['evidenceFileLocations']:
    #     Thread(target=work, args=('./'+key, ))

    return jsonify({})

