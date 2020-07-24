from flask import Blueprint, Response, request, jsonify
from serialize import serialize
import setting
import boto3

# scene: events/{event_id}/{scene_id}/{scene_file_location}
# evide: events/{event_id}/{scene_id}/{evidence_id}/{evidence_file_location}

s3 = boto3.resource('s3',
aws_access_key_id=setting.aws_access_key_id,
aws_secret_access_key=setting.aws_secret_access_key)

bucket = s3.Bucket(setting.img_bucket_name)

# for file in bucket.objects.all():
#     print(file.key)

app = Blueprint('server', __name__, url_prefix='/')

@app.route('/ping/', methods=['GET'])
def ping():
    return Response('OK', mimetype='text/plain')

@app.route('/matching/', methods=['POST'])
def featureMatching():
    value = request.get_json(silent=True)

    return jsonify(serialize(value))

