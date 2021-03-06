# microblog_flask_learn
from mega-tutorial Flask


1 переменная среды FLASK_APP: export FLASK_APP=microblog.py
  режим отладки:              export FLASK_DEBUG=1

________________________________________________________________
2
--------------------------------------------------------------------------------
3
--------------------------------------------------------------------------------
4
--------------------------------------------------------------------------------
5
--------------------------------------------------------------------------------
7 Часть 7: Обработка ошибок

-- Режим отладки

Но когда вы разрабатываете приложение, вы можете включить режим отладки, режим, в котором Flask выводит действительно хороший отладчик непосредственно в ваш браузер. Чтобы активировать режим отладки установите следующую переменную среды:

$ export FLASK_DEBUG=1 # linux
$ set FLASK_DEBUG=1  # win


-- Пользовательские страницы ошибок

Чтобы объявить пользовательский обработчик ошибок, используется декоратор @errorhandler. Создать новый модуль app/errors.py.

пример:
    from flask import render_template
    from app import app, db

    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('404.html'), 404

функция возвращают второе значение после шаблона, который является номером кода ошибки

    Вот шаблон для ошибки 404:

        {% extends "base.html" %}

        {% block content %}
            <h1>File Not Found</h1>
            <p><a href="{{ url_for('index') }}">Back</a></p>
        {% endblock %}


добавить импорт в app/__init__.py
    from app import routes, models, errors



-- logger 
  https://habr.com/ru/post/346880/

Отправка ошибок по электронной почте:
    from logging.handlers import SMTPHandler

Отправка ошибок в лог-файл
    from logging.handlers import RotatingFileHandler

категории ведения журнала, это DEBUG, INFO, WARNING,ERROR и CRITICAL




---------------------------------------------------------------------------------
8 Базы данных

https://habr.com/ru/post/347450/

-Один ко многим ( One-to-Many )
Двумя объектами, связанными этим отношением, являются пользователи и сообщения. Видим, что у пользователя много сообщений, а у сообщения есть один пользователь (или автор). Связь представлена ​​в базе данных с использованием внешнего ключа foreign key на стороне «много». В вышеприведенной связи внешний ключ — это поле user_id, добавленное в таблицу сообщений posts.
Это поле связывает каждое сообщение с записью его автора в пользовательской таблице.


-Многие-ко-многим ( Many-to-Many )
Представление многозначного представления, many-to-many требуют использования вспомогательной таблицы, называемой таблицей ассоциаций association table. 


-«Много-к-одному» и «один-к-одному» ( Many-to-One and One-to-One )

Много-к-одному похоже на отношение один-ко-многим. Разница в том, что эта связь рассматривается со стороны «Много».

Один-к-одному — частный случай «один ко многим». Представление аналогично, но в базу данных добавляется ограничение, чтобы предотвратить сторону «Много», запрещающее иметь более одной ссылки.
Хотя бывают случаи, когда этот тип отношений полезен, но он не так распространен, как другие типы.



--объединение запросов
[query1].union([query2])

    def followed_posts(self):
        followed = Post.query.join(
            followers, (followers.c.followed_id == Post.user_id)).filter(
            followers.c.follower_id == self.id)
        own = Post.query.filter_by(user_id=self.id)
        return followed.union(own).order_by(Post.timestamp.desc())
-------------------------------------------------------------------------------
9 разбиение на страницы
паттерн "Post/Redirect/Get" - Он избегает вставки повторяющихся сообщений, когда пользователь непреднамеренно обновляет страницу после отправки веб-формы.



-- pagination

 Flask-SQLAlchemy поддерживает разбиение на страницы изначально методом запроса paginate(). Если, например, мне надо получить первые двадцать записей пользователя, я могу заменить вызов all() в конце запроса:

>>> user.followed_posts().paginate(1, 20, False).items

Метод paginate можно вызвать для любого объекта запроса из Flask-SQLAlchemy. Это требует трех аргументов:

-номер страницы, начиная с 1
-количество элементов на странице
-флаг ошибки. Если True, когда запрашивается страница вне диапазона, 404 ошибка будет автоматически возвращена клиенту. Если False, пустой список будет возвращен для страниц вне диапазона.
Возвращаемое значение из paginate — объект Pagination. Атрибут items этого объекта содержит список элементов на запрошенной странице


page = request.args.get('page', 1, type=int) # получить текущую страницу или 1ю


- навигация по странице:

у объекта Pagination есть несколько других атрибутов, которые полезны при создании ссылок на страницы (помимо items):


has_next: True, если после текущей есть хотя бы одна страница
has_prev: True, если есть еще одна страница перед текущей
next_num: номер страницы для следующей страницы
prev_num: номер страницы для предыдущей страницы



| интересный аспект функции url_for() заключается в том,
| что вы можете добавить к нему любые аргументы ключевого слова, и если имена этих
| аргументов напрямую не указаны в URL-адресе, тогда Flask будет включать их в URL-
| адрес как аргументы запроса.


-----------------------------------------------------------------------------------
10 Поддержка электронной почты

конфиг почты:
    class Config(object):
        # ...
        MAIL_SERVER = os.environ.get('MAIL_SERVER')
        MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
        MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
        MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
        MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
        ADMINS = ['your-email@example.com']

os.environ.get -- получить значение установленное в переменной среды

Переменные конфигурации для электронной почты содержат сервер и порт, флаг для включения зашифрованных соединений и необязательное имя пользователя и пароль. Пять переменных конфигурации получены из их сопоставлений переменным среды. Если сервер электронной почты не установлен в среде, то я буду использовать это как знак того, что ошибки электронной почты должны быть отключены. Порт сервера электронной почты также можно указать в переменной среды, но если он не установлен, используется стандартный порт 25. Учетные данные почтового сервера по умолчанию не используются, но могут быть предоставлены при необходимости. Переменная конфигурации ADMINS представляет собой список адресов электронной почты, которые будут получать отчеты об ошибках, поэтому ваш собственный адрес электронной почты должен быть в этом списке.

пример:
        настроить настоящий почтовый сервер. Ниже приведена конфигурация для использования
        почтового сервера для учетной записи Gmail:


        export MAIL_SERVER=smtp.googlemail.com
        export MAIL_PORT=587
        export MAIL_USE_TLS=1
        export MAIL_USERNAME=<your-gmail-username>
        export MAIL_PASSWORD=<your-gmail-password>


flask-mail -- отправка эл почты

Ссылки на сброс пароля должны содержать в себе безопасный токен. Чтобы сгенерировать эти токены, использовать JSON Web Tokens, который также имеет популярный пакет для Python:

(venv) $ pip install pyjwt

Как и для большинства расширений Flask, вам нужно создать экземпляр сразу после создания приложения Flask. В этом случае это объект класса Mail:


        # ...
        from flask_mail import Mail

        app = Flask(__name__)
        # ...
        mail = Mail(app)


    Очень важно что бы строка mail = Mail(app) располагалась после
    app.config.from_object(Config).

использовать эмулированный почтовый сервер, то Python предоставляет вариант для запуска во втором терминале с помощью следующей команды:


    (venv) $ python -m smtpd -n -c DebuggingServer localhost:8025
Чтобы настроить этот сервер, необходимо установить две переменные среды:


    (venv) $ export MAIL_SERVER=localhost
    (venv) $ export MAIL_PORT=8025


отправить электронное письмо из оболочки Python:


    >>> from flask_mail import Message
    >>> from app import mail
    >>> msg = Message('test subject', sender=app.config['ADMINS'][0],
    ... recipients=['your-email@example.com'])
    >>> msg.body = 'text body'
    >>> msg.html = '<h1>HTML body</h1>'
    >>> mail.send(msg)




+ +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
+ существуют два типа контекстов, контекст приложения и контекст запроса (application         +
+ context и request context). В большинстве случаев эти контексты автоматически управляются
+ инфраструктурой, но когда приложение запускает пользовательские потоки, контексты для этих 
+ потоков могут потребовать ввода вручную.
+ Существует множество расширений, для которых требуется, чтобы контекст приложения работал, потому что
+ это позволяет им найти экземпляр приложения Flask без его передачи в качестве аргумента. Причина, по
+ которой многие расширения должны знать экземпляр приложения, заключается в том, что они имеют
+ конфигурацию, хранящуюся в объекте app.config. Это как раз ситуация с Flask-Mail. Метод mail.send()
+ должен получить доступ к значениям конфигурации для почтового сервера, и это может быть сделано 
+ только зная, что такое app. Контекст приложения, созданный с вызовом with app.app_context(), делает
+ экземпляр приложения доступным через переменную current_app из Flask.
+ +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

-------------------------------------------------------------------------------------------------
11 email
-------------------------------------------------------------------------------------------------
12 Даты и время
-- Конверсия часовых поясов

существует два способа использовать информацию о часовом поясе, доступную через JavaScript:


    Подход «старой школы» заключался бы в том, чтобы веб-браузер каким-то образом отправлял информацию о часовом поясе на сервер, когда пользователь впервые регистрируется в приложении. Это можно сделать с помощью вызова Ajax или, что еще проще, с тегом meta refresh. Как только сервер определил часовой пояс, он может сохранить его в сеансе или записать его в запись пользователя в базе данных, а затем настроить все временные метки во время отображения шаблонов.


    Подход «новой школы» состоял бы в том, чтобы не изменить ситуацию на сервере и позволить конвертировать с UTC в локальный часовой пояс на клиенте, используя JavaScript.
Оба варианта рабочие, но второй имеет большое преимущество. Знать часовой пояс не всегда достаточно, чтобы представить дату и время в ожидаемом пользователем формате. Браузер также имеет доступ к конфигурации локали системы, которая определяет такие вещи, как AM/PM и 24-часовой формат, DD/MM/YYYY против MM/DD/YYYY и многие другие культурные или региональные стили.

Moment.js — небольшая библиотека JavaScript с открытым исходным кодом переводит задачу отображения даты и времени совсем на другой уровень, так как предоставляет все мыслимые варианты форматирования. И некоторое время назад я создал Flask-Moment, небольшое расширение Flask, которое упростило включение Moment.js в ваше приложение.


Итак, начнем с установки Flask-Moment:


(venv) $ pip install flask-moment

Это расширение добавляется в приложение Flask обычным способом:


app/__init__.py: Создаем экземпляр Flask-Moment.

    # ...
    from flask_moment import Moment

    app = Flask(__name__)
    # ...
    moment = Moment(app)

Flask-Moment работает вместе с moment.js

app/templates/base.html: Добавляем moment.js в базовый шаблон.

...

{% block scripts %}
    {{ super() }}   #  добавить библиотеку moment.js, не теряя базового содержимого
    {{ moment.include_moment() }}
{% endblock %}


-Использование Moment.js

Moment.js предоставляет браузеру доступный moment class. Первым шагом для создания временной метки является создание объекта этого класса, передачей требуемой метки времени в формате ISO 8601. Вот пример:


t = moment('2017-09-28T21:45:23Z')

Если вы не знакомы со стандартным форматом ISO 8601 для дат и времени, формат выглядит следующим образом: {{ year }}-{{ month }}-{{ day }}T{{ hour }}:{{ minute }}:{{ second }}{{ timezone }}

тобразить дату на языке отличающемся от английского, например русском. Расширение flask-moment имеет для этой цели в своем арсенале метод lang()
{% block scripts %}
    {{ super() }}
    {{ moment.include_moment() }}
    {{ moment.lang('ru') }}     <!-- Я добавил эту строку -->
{% endblock %}
----------------------------------------------------------------------------------

13 translate 

& pip install flask-babel

    # ...
    from flask_babel import Babel

    app = Flask(__name__)
    # ...
    babel = Babel(app)

Чтобы отслеживать список поддерживаемых языков, следует добавить переменную конфигурации:
config.py: Список поддерживаемых языков.

    class Config(object):
        # ...
        LANGUAGES = ['en', 'es']

Экземпляр Babel предоставляет декоратор localeselector. Декорированная функция вызывается для каждого запроса, чтобы выбрать перевод языка для использования:


app/__init__.py: Выбор предпочтительного языка.

        from flask import request

        # ...

        @babel.localeselector
        def get_locale():
            return request.accept_languages.best_match(app.config['LANGUAGES'])



--Усовершенствования для командной строки (part 13)

Легко добавить специфичные для приложения команды в flask. 
Flask полагается на Click для всех своих операций с командной строкой. Команды, такие как translate, которые являются корнем для нескольких подкоманд, создаются с помощью декоратора app.cli.group(). Я собираюсь поместить эти команды в новый модуль под названием app/cli.py:


app/cli.py: Перевести группу команд.

    from app import app

    @app.cli.group()
    def translate():
        """Translation and localization commands."""
        pass

app/cli.py: Обновление и компиляция вложенных команд.

import os

    # ...

    @translate.command()
    def update():
        """Update all languages."""
        if os.system('pybabel extract -F babel.cfg -k _l -o messages.pot .'):
            raise RuntimeError('extract command failed')
        if os.system('pybabel update -i messages.pot -d app/translations'):
            raise RuntimeError('update command failed')
        os.remove('messages.pot')

    @translate.command()
    def compile():
        """Compile all languages."""
        if os.system('pybabel compile -d app/translations'):
            raise RuntimeError('compile command failed')

-- AJAX
Что такое AJAX?
Ajax означает Асинхронный JavaScript и XML. В основе технологии лежит использование нестандартного объекта XMLHttpRequest, необходимого для взаимодействия со скриптами на стороне сервера. Объект может как отправлять, так и получать информацию в различных форматах включая XML, HTML и даже текстовые файлы. Самое привлекательное в Ajax — это его асинхронный принцип работы. С помощью этой технологии можно осуществлять взаимодействие с сервером без необходимости перезагрузки страницы. Это позволяет обновлять содержимое страницы частично, в зависимости от действий пользователя.

--------------------------------------------------------------------------------------------------

15 Blueprint + unittest undder blueprint


--------------------------------------------------------------------------------------------------

16 search

    pip install flask-msearch
    # when MSEARCH_BACKEND = "whoosh"
    pip install whoosh blinker


Quickstart
    from flask_msearch import Search
    [...]
    search = Search()
    search.init_app(app)

    # models.py
    class Post(db.Model):
        __tablename__ = 'post'
        __searchable__ = ['title', 'content']

Config
    # when backend is elasticsearch, MSEARCH_INDEX_NAME is unused
    # flask-msearch will use table name as elasticsearch index name unless set __msearch_index__
    MSEARCH_INDEX_NAME = 'msearch'
    # simple,whoosh,elaticsearch, default is simple
    MSEARCH_BACKEND = 'whoosh'
    # table's primary key if you don't like to use id, or set __msearch_primary_key__ for special model
    MSEARCH_PRIMARY_KEY = 'id'
    # auto create or update index
    MSEARCH_ENABLE = True
    # logger level, default is logging.WARNING
    MSEARCH_LOGGER = logging.DEBUG
    # SQLALCHEMY_TRACK_MODIFICATIONS must be set to True when msearch auto index is enabled
    SQLALCHEMY_TRACK_MODIFICATIONS = True



if raise sqlalchemy ValueError,please pass db param to Search

db = SQLalchemy()
search = Search(db=db)

Create_index
    search.create_index()
    search.create_index(Post)
Update_index
    search.update_index()
    search.update_index(Post)
    # or
    search.create_index(update=True)
    search.create_index(Post, update=True)
Delete_index
    search.delete_index()
    search.delete_index(Post)
    # or
    search.create_index(delete=True)
    search.create_index(Post, delete=True)


query:
    Post.query.msearch('searchable text').all()


















