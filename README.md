# pjt04 - 프레임워크 기반 웹페이지 구현



## 1. 목표

- 기본 CRUD 기능이 있는 Web Application 제작
- Python Web Framework를 통한 데이터 조작
-  Object Relational Mapping(ORM)에 대한 이해
- 관리자 페이지를 통한 관리



## 2. 개발 환경

- Python 3.8.7
- Django 3.1.7
- vsCode



## 3. 구현 내용

#### A. 가상 개발 환경 구축

- 가상환경 만들기

  ```bash
  # terminal
  python -m venv venv
  ```

- 가상환경 시작하기

  ```bash
  source venv/Script/activate
  ```

- 가상환경에 djanggo 설치하기

  ```bash
  pip install django
  ```

- 가상환경에 설치된 라이브러리들 모두 requirements.txt에 기록하기 (다른 컴퓨터에서 작업할 때 같은 개발환경을 쉽게 구축하기 위해 requirements.txt를 만들어둔다.)

  ```bash
  pip freeze > requirements.txt
  
  # requirements.txt에 기록된 라이브러리들 모두 설치하는 명령어
  # pip install -r requirements.txt
  ```



#### B. Model

- project 생성

  ```bash
  # terminal
  django-admin startproject pjt04
  ```

- application 생성

  ```bash
  # terminal
  python manage.py startapp movies
  ```

- Model 정의

  ```python
  # movies/models.py
  from django.db import models
  
  class Movie(models.Model):
      objects = models.Manager()
      title = models.CharField(max_length=100)	# 제목
      overview = models.TextField()	# 줄거리
      poster_path = models.CharField(max_length=500)	# 포스트 경로
  ```

- Model -> DB의 table 생성

  ```bash
  # terminal
  
  # migraion 만들기 (설계도 생성)
  python manage.py makemigrations
  
  # DB로 옮기기 (설계도를 바탕으로 sql에 구조 만들기)
  python manage.py migrate
  ```

- DB에 data load하기

  ```bash
  # terminal
  
  # movies.json은 제공되었음
  python manage.py loaddata movies.json
  ```



#### C. Admin

- Admin 계정 만들기

  ```bash
  # terminal
  python manage.py createsuperuser
  Username : admin
  Email address : 
  Password : 
  Password (again) :
  ```

- Admin 페이지에 Movie Data 등록

  ```python
  # movies/admin.py
  from django.contrib import admin
  from .models import Movie
  
  class MovieAdmin(admin.ModelAdmin):
      list_display = ('pk', 'title', 'overview', 'poster_path')
      
  admin.site.register(Movie, MovieAdmin)
  ```

- Admin url 경로 (프로젝트 생성시 기본으로 만들어짐)

  ```python
  # pjt04/urls.py
  from django.contrib import admin
  
  urlpatterns = [
      path('admin/', admin.site.urls),
  ]
  ```

  

#### D. URL

- movies 경로를 movies앱에서 따로 관리 

  ```python
  # pjt04/urls.py
  from django.contrib import admin
  from django.urls import path, include
  
  urlpatterns = [
      path('admin/', admin.site.urls),
      path('movies/', include('movies.urls')),
  ]
  ```

- movies의 url 패턴

  ```python
  # movies/urls.py
  from django.urls import path
  from . import views
  
  app_name = 'movies'
  
  urlpatterns = [
      path('', views.index, name='index'),	# 전체 영화 목록 조회
      path('new/', views.new, name='new'),	# 새로운 영화 작성 Form
      path('create/', views.create, name='create'),	# 새로운 영화 데이터 저장
      path('<int:pk>/', views.detail, name='detail'),	# 단일 영화 상세 조회
      path('<int:pk>/edit', views.edit, name='edit'),	# 단일 영화 수정 Form
      path('<int:pk>/update', views.update, name='update'),	# 수정된 영화 데이터 저장
      path('<int:pk>/delete', views.delete, name='delete'),	# 단일 영화 삭제
  ]
  ```



#### E. View & Template

- 공유 템플릿 생성 및 사용

  1. 모든 HTMl 파일은 base.html을 확장(extends)하여 사용
  2. base.html은 모든 페이지가 공유하는 상단 네비게이션 바를 표시
  3. 네비게이션 바는 전체 영화 목록 조회 페이지(movies:index)와 새로운 영화 작성 페이지(movies:new)로 이동할 수 있는 링크를 포함

  ```django
  <!-- pjt04/templates/base.html -->
  <!DOCTYPE html>
  <html lang="en">
  <head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <!-- bootstrap CDN -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-BmbxuPwQa2lc/FVzBcNJ7UAyJxM6wuqIj61tLrc4wSX0szH/Ev+nYRRuWlolflfl" crossorigin="anonymous">
    <title>Document</title>
  </head>
  <body>
    <!-- 네비게이션 바 -->
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
    <div class="container-fluid">
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav">
          <li class="nav-item">
            <a class="nav-link" href="{% url 'movies:index' %}">INDEX</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="{% url 'movies:new' %}">NEW</a>
          </li>
        </ul>
      </div>
    </div>
    </nav>
    
      <!-- 다른 HTML 파일에 필요한 content를 넣을 block -->
    <div class="container">
      {% block content %}
      {% endblock content %}
    </div>
    <!-- bootstrap CDN -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta2/dist/js/bootstrap.bundle.min.js" integrity="sha384-b5kHyXgcpbZJO/tY9Ul7kGkf1S0CWuKcCD38l8YkeH8z8QjE0GmW1gYU5S9FOnJ0" crossorigin="anonymous"></script>
  </body>
  </html>
  ```

- 전체 영화 목록 조회

  1. 데이터베이스에 존재하는 모든 영화의 목록을 표시
  2. 사용자에게 응답으로 제공할 HTML 파일 : index.html
  3. title, 포스터 이미지 표시
  4. title 클릭 시 해당 영화의 상세 조회 페이지(movies:detail)로 이동

  ```python
  # movies/urls.py
  path('', views.index, name='index'),
  ```

  ```python
  # movies/views.py
  from django.shortcuts import render, redirect
  from .models import Movie
  
  def index(request):
      movies = Movie.objects.all()
      context = {
          'movies':movies,
      }
      return render(request, 'movies/index.html', context)
  ```

  ```django
  <!-- movies/templates/movies/index.html -->
  {% extends 'base.html' %}
  
  {% block content %}
    <h1>INDEX PAGE</h1>
    {% for movie in movies %}
      <a href="{% url 'movies:detail' movie.pk %}">{{ movie.title }}</a>
      <img src="{{ movie.poster_path }}" alt="영화 포스터">
      <hr>
    {% empty %}
      <p>영화가 없습니다.</p>
    {% endfor %}
  {% endblock content %}
  ```

- 새로운 영화 작성 Form

  1. 사용자에게 응답으로 제공할 HTML 파일 : new.html
  2. 영화를 작성할 수 있는 Form을 표시
  3. Form에 작성한 정보는 submit시, 사용자 제출 데이터를 저장하는 URL(movies:create)로 요청과 함께 전송됨

  ```python
  # movies/urls.py
  path('new/', views.new, name='new'),
  ```

  ```python
  # movies/views.py
  def new(request):
      return render(request, 'movies/new.html')
  ```

  ```django
  <!-- movies/templates/movies/new.html -->
  {% extends 'base.html' %}
  
  {% block content %}
    <h1>NEW PAGE</h1>
    <form action="{% url 'movies:create' %}" method="POST">
      {% csrf_token %}
      <label for="title">TITLE : </label>
      <input type="text" id="title" name="title">
      <br>
  
      <label for="overviwe">OVERVIEW : </label>
      <textarea name="overview" id="overview" cols="30" rows="10"></textarea>
      <br>
  
      <label for="poster_path">POSTER_PATH : </label>
      <input type="text" id="poster_path" name="poster_path">
      <br>
  
      <input type="submit" value="생성">
    </form>
  {% endblock content %}
  ```

- 영화 데이터를 저장

  1. 요청과 함께 전송된 데이터를 데이터베이스에 저장
  2. 저장이 완료되면 저장한 영화의 상세 조회 페이지(movies:detail)로 Redirect

  ```python
  # movies/urls.py
  path('create/', views.create, name='create'),
  ```

  ```python
  # movies/views.py
  def create(request):
      # request에서 보내준  title, overview, poster_path 데이터 얻기
      title = request.POST.get('title')
      overview = request.POST.get('overview')
      poster_path = request.POST.get('poster_path')
      
  	# 전체 영화 목록 조회 페이지(movies:index)로 redirect하는 방법
      # Movie.objects.create(title=title, overview=overview, poster_path=poster_path)
      # return redirect('movies:index')
      
      # DB에 저장하기
      movie = Movie(title=title, overview=overview, poster_path=poster_path)
      movie.save()
      # 상세 조회 페이지(movies:detail)로 redirect하는 방법
      return redirect('movies:detail', movie.pk)
  ```

- 단일 영화 상세 조회

  1. URL을 통해 함께 전달된 pk에 해당하는 영화 상세정보를 HTML에 표시해야 함
  2. 사용자에게 응답으로 제공할 HTML : detail.html
  3. 영화의 title, overview, poster_path 표시

  ```python
  # movies/urls.py
  path('<int:pk>/', views.detail, name='detail'),
  ```

  ```python
  # models/views.py
  def detail(request, pk):
      movie = Movie.objects.get(pk=pk)
      context = {
          'movie': movie,
      }
      return render(request, 'movies/detail.html', context)
  ```

  ```django
  <!-- movies/templates/movies/detail.html -->
  {% extends 'base.html' %}
  
  {% block content %}
    <h1>DETAIL PAGE</h1>
    <hr>
    <p>TITLE : {{ movie.title }}</p>
    <p>OVERVIEW : {{ movie.overview }}</p>
    <p>POSTER_PATH : {{ movie.poster_path }}</p>
    <a href="{% url 'movies:edit' movie.pk %}">수정</a>
    <form action="{% url 'movies:delete' movie.pk %}" method="POST">
      {% csrf_token %}
      <input type="submit" value="삭제">
    </form>
  {% endblock content %}
  ```

- 단일영화 정보 수정 Form

  1. pk에 해당하는 영화 상세정보를 가져오고, 그 데이터를 수정할 수 있는 tag 필요
  2. 응답으로 제공할 HTML : edit.html

  ```python
  # movies/urls.py
  path('<int:pk>/edit', views.edit, name='edit'),
  ```

  ```python
  # movies/views.py
  def edit(request, pk):
      movie = Movie.objects.get(pk=pk)
      context = {
          'movie':movie
      }
      return render(request, 'movies/edit.html', context)
  ```

  ```django
  {% extends 'base.html' %}
  
  {% block content %}
    <h1>EDIT PAGE</h1>
    <hr>
    <form action="{% url 'movies:update' movie.pk %}" method="POST">
      {% csrf_token %}
      <label for="title">TITLE : </label>
      <input type="text" id="title" name="title" value="{{ movie.title }}">
      
      <label for="overview">OVERVIEW : </label>
      <textarea name="overview" id="overview" cols="30" rows="10">{{ movie.overview }}</textarea>
  
      <label for="poster_path">POSTER_PATH : </label>
      <input type="text" id="poster_path" name="poster_path" value="{{ movie.poster_path }}">
      
      <input type="submit" value="수정">
    </form>
    
  {% endblock content %}
  ```

- 수정된 영화 데이터 저장

  1. 요청과 함께 전송된 데이터를 해당 pk를 통해 model을 가져오고, 수정 후 다시 데이터베이스에 저장
  2. 저장이 완료되면 저장한 영화의 상세 조회 페이지(movies:detail)로 Redirect
  3. GET 방식으로 요청이 발생할 경우, DB에 data가 load되는 것을 방지하기 위해,  영화 정보 수정 Form(movies:edit)페이지로 Redirect

  ```python
  # movies/urls.py
  path('<int:pk>/update', views.update, name='update'),
  ```

  ```python
  # movies/views.py
  def update(request, pk):
      if request.method == 'POST':
          title = request.POST.get('title')
          overview = request.POST.get('overview')
          poster_path = request.POST.get('poster_path')
  
          movie = Movie.objects.get(pk=pk)
          movie.title = title
          movie.overview = overview
          movie.poster_path = poster_path
          movie.save()
          return redirect('movies:detail', pk)
      
      return redirect('movies:edit', pk)
  ```

- 단일 영화 정보 삭제

  1. GET 방식의 요청이 발생하는 경우, 단일 영화 상세 조회 페이지(movies:detail)로 redirect (DB의 data가 삭제되는 것을 방지하기 위함)
  2. POST 방식의 요청이 발생하는 경우, 요청과 함께 전송된 pk 데이터를 통해 해당 row를 delete하고, 전체 영화 목록 조회페이지(movies:index)로 Redirect

  ```python
  # movies/urls.py
  path('<int:pk>/delete', views.delete, name='delete'),
  ```

  ```python
  # movies/views.py
  def delete(request, pk):
      if request.method == 'POST':
          movie = Movie.objects.get(pk=pk)
          movie.delete()
          return redirect('movies:index')
      else:
          return redirect('movies:detail', pk)
  ```

  

#### 어려웠던 부분

첫 협업 프로젝트라 가상 개발 환경을 구축했는데, 처음하는 작업이라 시간이 조금 걸렸다.

가상 개발 환경을 생성하고, 필요한 라이브러리들을 그 가상환경에 설치하고, 이를 다른 작업자가 설치하기 쉽게 하기 위해 freeze해 파일을 만들어 저장했다. 

테스팅을 위한 fixture를 따로 관리해야하기 때문에 DB는 gitignore시키고, DB의 데이터들만 dumpdata를 통해 json파일로 저장했다. 그리고 pull을 하는 동료는 json 파일을 loaddata해서 DB에 데이터들을 저장할 수 있었다.

 - DB를 따로 관리해야하는 이유는 뭘까..?
   	- Admin 계정이 공유되기 때문?
   	- 작업 테스트를 할 때, DB를 한명이 관리하고 있으면 그 사람이 runserver를 했을 때만 DB와 연결이 되기 때문?