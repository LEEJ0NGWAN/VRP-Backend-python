from flask import Blueprint, Response, request, jsonify
from serialize import serialize
from error_handler import Error, register_handler
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

app = Blueprint('s3_api', __name__)
register_handler(app)

@app.route('/ping/', methods=['GET'])
def ping():
    return Response('testsetsetset', mimetype='text/plain')


# TODO: s3 에러처리 하고 이미지 가져오기
@app.route('/matching/', methods=['POST'])
def featureMatching():
    data = request.get_json(silent=True)

    if 'sceneFileLocation' not in data\
    or 'evidenceFileLocations' not in data:
        raise Error(status_code=400)

    return jsonify(serialize(data))

