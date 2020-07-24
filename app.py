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
    return "hello!"



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

Error1
Could not locate a Flask application. You did not provide the "FLASK_APP" environment variable, and a "wsgi.py" or "app.py" module was not found in the current directory.


Error2
error: Your local changes to the following files would be overwritten by merge:
        app.py
        
        
git stash - 내가 여태까지 진행한 변경사항을 "임시"로 저장(=은닉 시켜놓는 것)
          - 로컬 기준으로 최신 브랜치에서 변경된 사항(git status 시 modified 되있는것)
          - 버전 관리도 가능하지만, 그런 복잡한 것은 아직 지양
git stash apply - stash 해놓은 변경사항들을 다시 반영(pull한 이후에 사용 해보기)

.gitignore는 origin repository에 올라간 파일에는 효과가 없다.
이유는 없다. 그냥 그렇다.
gitignore가 통하지 않는 이런 파일들은 올리고 싶지 않은데 어떻게 하는게 좋을까?
git update-index --assume-unchanged "파일 이름" : 해당파일의 변화를 git에서 감지하지 않는다고 명시.

"""

