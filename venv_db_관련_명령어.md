# venv(가상환경), DB 관련 명령어



가상환경 만들기

```bash
python -m venv venv
```



가상환경 실행하기

```bash
source venv/Scripts/activate
```



라이브러리 확인

```bash
pip list
```



requirements.txt에 있는 라이브러리들 모두 설치하기

```bash
pip install -r requirements.txt
```



django 라이브러리 설치

```bash
pip install django
```



설치한 라이브러리 정보 가져와서 requirements.txt에 넣기

```bash
pip freeze > requirements.txt
```



가상환경 종료하기

```bash
deactivate
```



DB 만들기 (repository에서 git pull을 하면 -> model과 migration은 있지만, DB에 table은 git ignore 되어있기 때문)

```bash
python manage.py migrate
```



movies.json에 있는 data를 복사해서 DB의 table에 넣기

```bash
python manage.py loaddata
```



DB에서 data를 복사해서 가져와서 movies.json에 넣기 (movies.json이 없으면 파일을 만들어서 넣는다.)

```bash
python manage.py dumpdata --indent 4 movies.movie > movies.json
```

