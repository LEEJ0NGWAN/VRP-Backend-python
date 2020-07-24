import setting
from flask import Flask
import boto3

app = Flask(__name__)
s3 = boto3.resource('s3',
    aws_access_key_id=setting.aws_access_key_id,
    aws_secret_access_key=setting.aws_secret_access_key)

my_bucket = s3.Bucket(setting.img_bucket_name)

for file in my_bucket.objects.all():
    print(file.key)

@app.route("/")
def hello():
    return body



"""
boto3 : AWS의 서비스들을 S3, SQL .... 파이썬에서 접근하기 위해서 존재하는 라이브러리
localhost:5000/    -> 플라스크는 기본 포트로 5000번 사용

$ set ENV_VARIABLE : 윈도우즈 환경변수 설정 명령어
APP_FLASK="실행 파일 이름" : 환경변수로 이 설정을 해줘야 flask run 명령어를 알아 들음.
AWS_ACCESS_KEY_ID = AWS *.csv로 받은 액세스 키
SECRET_ACCESS_KEY= AWS *.csv로 받은 시크릿 키
.csv 파일은 졸업 프로젝트 폴더에 같이 모아뒀다.

$ flask run : 환경변수에 등록된 실행파일 이름으로 플라스크가 실행 됨

s3 버켓에 타인에게 권한을 허락하려면 타인의 정규 사용자 해시 코드가 필요하다.
aws 웹 콘솔에서 정규 사용자 해시 코드를 등록하여 타인에게 s3 접근 권한을 허가하였다.
IAM 권한(=s3 접근권한)을 등록하면 타인의 s3 버켓도 내 것으로 인식한다

내 버켓에 vrp-s3는 없지만 인식이 된다!
s3=boto3.client('s3')


 Could not locate a Flask application. You did not provide the "FLASK_APP" environment variable, and a "wsgi.py" or "app.py" module was not found in the current directory.

"""

