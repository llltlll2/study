 # Django 勉強


 ## プロジェクト
 * urls.py アプリ自体のパスの指定とどのそれに対してどのurls を持って来るかの指定
 ```python:mysite/urls.py
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("polls/", include("polls.urls")),
    path("admin/", admin.site.urls),
]
 ```
 ## アプリケーション
 * view.py 具体的な中身（ロジック）の記述（どういうのを出力するか）
```python:myapp/view.py
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")
 ```

 * urls.py パスの名前とviewのクラスの何を使うのかの記述
  ```python:myapp/urls.py
polls/urls.py¶
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
]
 ```

 ## path()関数について
引数が4つある  
route と view はそれぞれ必須  
 * route
   * routeはURLパターンを含む文字列を指定する
   * Django は urlpatterns のはじめのパターンから開始し、リストを順に下に見ていきます。要求された URL を一致するものを見つけるまで各パターンと比較します
 * view
   * マッチする正規表現を見つけるとview関数を呼び出す。
 * kwargs
   * 任意のキーワードを辞書として対象のビューにわたすことができる
 * name
   * URLに名付ける  
特にテンプレートに持ってくる際に有効  
どういうこと?  
URLを変えたとしても変える部分をURLを変えるだけにできる