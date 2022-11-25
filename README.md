# YoutubeScraper
<style>
img[alt=ineuron_logo] { 
    width: 70px;
    margin-bottom: -6px;
}
</style>


# YoutubeScraper

This is a first project from [![ineuron_logo](https://ineuron.ai/images/ineuron-logo-white.png)](https://ineuron.ai/)


## Project description

#### Project is to, 

  - Collect data from Youtube and store them in both SQL and NoSQL,
  - Make web application that show collected data
  - Deployee web app on AWS, Azure, GCP, or Heroku


## Approach and Tech stack

  - **Python:** high-level, general-purpose programming language.
  - **Django:** Python-based web framework that follows the Model–Template–Views architectural pattern.
  - **Database:** 
    - SQL: Postgres, to store id, title, likes, views etc...
    - NoSQL: MongoDB, to store thumbnail(url or base64), long text(comment, description), etc...

## Demo

#### Live demo: [yts-by-mg.herokuapp.com](yts-by-mg.herokuapp.com)

## URL Reference

- ### Search video
  ```http
    GET /results
  ```
  | Parameter      | Type     | Default     | Description                |
  | :------------- | :------- | :---------- | :------------------------- |
  | `search_query` | `str`    | **Not Set** | **Required**. Keyword of video |

- ### Channel videos
  ```http
    GET /channel/<c_id>
  ```
  | Parameter      | Type     | Default     | Description                |
  | :------------- | :------- | :---------- | :------------------------- |
  | `c_id`         | `str`    | **Not Set** | **Required**. channel Id |

- ### Watch video
  ```http
    GET /watch
  ```
  | Parameter      | Type     | Default     | Description                |
  | :------------- | :------- | :---------- | :------------------------- |
  | `v`            | `str`    | **Not Set** | **Required**. Video Id |



## Environment Variables

To run this project, you will need to add the following environment variables to your `YoutubeScraper\envs\Dev.env` file

| Key                       | Type     | Description         |
| :------------------------ | :------- | :------------------ |
| ALLOWED_HOSTS             | `str`    | A list of strings representing the host/domain names that this Django site can serve. |
| DEBUG                     | `bool`   | A boolean that turns on/off debug mode. |
| DEFAULT_LOGGER_LEVEL      | `str`    | Describes the severity of the messages that the logger will handle. |
| DJANGO_SUPERUSER_EMAIL    | `str`    | Create superuser in non-interactive mode |
| DJANGO_SUPERUSER_PASSWORD | `str`    | Create superuser in non-interactive mode. |
| DJANGO_SUPERUSER_USERNAME | `str`    | Create superuser in non-interactive mode. |
| MONGO_CLUSTER             | `str`    | Cluster name of MongoDB |
| MONGO_DB_NAME             | `str`    | Database name on MongoDB |
| MONGO_PASSWORD            | `str`    | Access password of MongoDB |
| MONGO_USERNAME            | `str`    | Username of MongoDB |
| SCRAPER_LOGGER_LEVEL      | `str`    | app vis logging level |
| SECRET_KEY                | `str`    | provide cryptographic signing session cookies. |
| YT_API_KEY                | `str`    | Access YouTube’s data in a more comprehensive way |



## Run Locally

Clone the project

```bash
  git clone https://link-to-project
```

Go to the project directory

```bash
  cd YoutubeScraper
```

Install dependencies

```bash
  pip install -r requirements.txt
```

Make new migrations if required

```bash
  python manage.py makemigrations
```

Applying migrations

```bash
  python manage.py migrate
```

Create superuser from environment variable

```bash
  # for fresh superuser, remove --no-input option
  python manage.py createsuperuser --no-input
```

Run local server

```bash
  python manage.py runserver
```


## Roadmap

- #### colorful log messages

    | log attributes | ASCII | Hex                                                                |
    | -------------- | ----- | ------------------------------------------------------------------ |
    | NOSET          |  15   | ![#d0d0d1](https://via.placeholder.com/10/d0d0d1?text=+) #d0d0d1 |
    | DEBUG          |  51   | ![#05dede](https://via.placeholder.com/10/05dede?text=+) #05dede |
    | INFO           |  27   | ![#0556de](https://via.placeholder.com/10/0556de?text=+) #0556de |
    | WARNING        |  208  | ![#de7805](https://via.placeholder.com/10/de7805?text=+) #de7805 |
    | CRITICAL       |  196  | ![#de0505](https://via.placeholder.com/10/de0505?text=+) #de0505 |
    | ERROR          |  197  | ![#de0556](https://via.placeholder.com/10/de0556?text=+) #de0556 |
    | module         |  221  | ![#dbba54](https://via.placeholder.com/10/dbba54?text=+) #dbba54 |
    | class          |  203  | ![#db5454](https://via.placeholder.com/10/db5454?text=+) #db5454 |
    | function       |  41   | ![#02ba54](https://via.placeholder.com/10/02ba54?text=+) #02ba54 |
    | lineno         |  200  | ![#de05bc](https://via.placeholder.com/10/de05bc?text=+) #de05bc |
    | message        |  15   | ![#d3d3d3](https://via.placeholder.com/10/d3d3d3?text=+) #d3d3d3 |
    | parameter      |  117  | ![#7bb6d3](https://via.placeholder.com/10/7bb6d3?text=+) #7bb6d3 |
    | stack_info     |  229  | ![#dede9a](https://via.placeholder.com/10/dede9a?text=+) #dede9a |
    | exception_info |  124  | ![#9a0505](https://via.placeholder.com/10/9a0505?text=+) #9a0505 |



- #### change app level setting from admin interface
  by creating separate database model 

  | key | value | description |
  | --- | ----- | ----------- |
  |	MAX_VIDEOS_FROM_CHANNEL |	10 | maximum videos from channel to fetch data |




- #### access log within admin interface
  - option 1: put log message directly into database, doing this database hit every time when log message created. othervis you can create queue in LogHandler class (not instance) and bukl_create once queue is full.
  - option 2: put log message in file, put those files in cluod and download file from admin interfase




<!-- ## Project tree -->

<!-- ```
YoutubeScraper
|
|  .gitignore
|  loggger.log
|  manage.py
|  Procfile
|  README.md
|  requirements.txt
|  runtime.txt
|
+----------------------------------------------------------------------assets
|                                                                      +--media
+----------------------------------------backend                       |    .gitkeep
|                                        |  __init__.py                |
+-----------------------envs             |  asgi.py                    \--staticfiles
|                         Dev.env        |  urls.py                    +--admin
\--multiapps              Prod1.env      |  wsgi.py                    |  +--css
   +--core                                  |                          |  |  |  autocomplete.css
   |  |  __init__.py                        \--settings                |  |  |  base.css
   |  |  apps.py                                 __init__.py           |  |  |  changelists.css
   |  |  models.py                               _base.py              |  |  |  dark_mode.css
   |  |  signals.py                              local.py              |  |  |  dashboard.css
   |  |  tests.py                                log_formatter.py      |  |  |  fonts.css
   |  |                                          prod.py               |  |  |  forms.css
   |  +--admin                                                         |  |  |  login.css
   |  |    __init__.py                                                 |  |  |  nav_sidebar.css
   |  |    _actions.py                                                 |  |  |  responsive.css
   |  |    _admin.py                                                   |  |  |  responsive_rtl.css
   |  |                                                                |  |  |  rtl.css
   |  +--fixtures                                                      |  |  |  widgets.css
   |  |    db_backup_setting.json                                      |  |  |
   |  |                                                                |  |  \--vendor
   |  +--helpers                                                       |  |     \--select2
   |  |    __init__.py                                                 |  |          LICENSE-SELECT2.md
   |  |    utils.py                                                    |  |          select2.css
   |  |                                                                |  |          select2.min.css
   |  \--migrations                                                    |  |
   |       __init__.py                                                 |  +--fonts
   |       0001_initial.py                                             |  |    LICENSE.txt
   |                                                                   |  |    README.txt
   \--scraper                                                          |  |    Roboto-Bold-webfont.woff
      |  __init__.py                                                   |  |    Roboto-Light-webfont.woff
      |  apps.py                                                       |  |    Roboto-Regular-webfont.woff
      |  dbrouters.py                                                  |  |
      |  signals.py                                                    |  +--img
      |  tests.py                                                      |  |  |  calendar-icons.svg
      |  urls.py                                                       |  |  |  icon-addlink.svg
      |  views.py                                                      |  |  |  icon-alert.svg
      |                                                                |  |  |  icon-calendar.svg
      +--admin                                                         |  |  |  icon-changelink.svg
      |    __init__.py                                                 |  |  |  icon-clock.svg
      |    _actions.py                                                 |  |  |  icon-deletelink.svg
      |    _admin.py                                                   |  |  |  icon-no.svg
      |    _inlines.py                                                 |  |  |  icon-unknown-alt.svg
      |                                                                |  |  |  icon-unknown.svg
      +--helpers                                                       |  |  |  icon-viewlink.svg
      |    __init__.py                                                 |  |  |  LICENSE
      |    _youtubeapis.py                                             |  |  |  icon-yes.svg
      |    db_dispensers.py                                            |  |  |  inline-delete.svg
      |    extractors.py                                               |  |  |  README.txt
      |                                                                |  |  |  search.svg
      +--migrations                                                    |  |  |  selector-icons.svg
      |    __init__.py                                                 |  |  |  sorting-icons.svg
      |    0001_initial.py                                             |  |  |  tooltag-add.svg
      |                                                                |  |  |  tooltag-arrowright.svg
      +--models                                                        |  |  |
      |    __init__.py                                                 |  |  \--gis
      |    _mongo.py                                                   |  |       move_vertex_off.svg
      |    _sql.py                                                     |  |       move_vertex_on.svg
      |                                                                |  |
      \--templates                                                     |  \--js
        |  404.html                                                    |     |  actions.js
        |  500.html                                                    |     |  autocomplete.js
        |                                                              |     |  calendar.js
        \--scraper                                                     |     |  cancel.js
           |  base.html                                                |     |  change_form.js
           |  base_site.html                                           |     |  collapse.js
           |  index.html                                               |     |  core.js
           |  video_list.html                                          |     |  filters.js
           |  watch_video.html                                         |     |  inlines.js
           |                                                           |     |  jquery.init.js
           \--includes                                                 |     |  nav_sidebar.js
                tags.html                                              |     |  popup_response.js
                video_grid.html                                        |     |  prepopulate.js
                video_stream.html                                      |     |  prepopulate_init.js
                                                                       |     |  SelectBox.js
                                                                       |     |  SelectFilter2.js
                                                                       |     |  urlify.js
                                                                       |     |
                                                                       |     +--admin
                                                                       |     |    DateTimeShortcuts.js
                                                                       |     |    RelatedObjectLookups.js
                                                                       |     |
                                                                       |     \--vendor
                                                                       |        +--jquery
                                                                       |        |    jquery.js
                                                                       |        |    jquery.min.js
                                                                       |        |    LICENSE.txt
                                                                       |        |
                                                                       |        +--select2
                                                                       |        |  |  LICENSE.md
                                                                       |        |  |  select2.full.js
                                                                       |        |  |  select2.full.min.js
                                                                       |        |  |
                                                                       |        |  \--i18n
                                                                       |        |       af.js
                                                                       |        |       ar.js
                                                                       |        |       az.js
                                                                       |        |       bg.js
                                                                       |        |       bn.js
                                                                       |        |       bs.js
                                                                       |        |       ca.js
                                                                       |        |       cs.js
                                                                       |        |       da.js
                                                                       |        |       de.js
                                                                       |        |       dsb.js
                                                                       |        |       el.js
                                                                       |        |       en.js
                                                                       |        |       es.js
                                                                       |        |       et.js
                                                                       |        |       eu.js
                                                                       |        |       fa.js
                                                                       |        |       fi.js
                                                                       |        |       fr.js
                                                                       |        |       gl.js
                                                                       |        |       he.js
                                                                       |        |       hi.js
                                                                       |        |       hr.js
                                                                       |        |       hsb.js
                                                                       |        |       hu.js
                                                                       |        |       hy.js
                                                                       |        |       id.js
                                                                       |        |       is.js
                                                                       |        |       it.js
                                                                       |        |       ja.js
                                                                       |        |       ka.js
                                                                       |        |       km.js
                                                                       |        |       ko.js
                                                                       |        |       lt.js
                                                                       |        |       lv.js
                                                                       |        |       mk.js
                                                                       |        |       ms.js
                                                                       |        |       nb.js
                                                                       |        |       ne.js
                                                                       |        |       nl.js
                                                                       |        |       pl.js
                                                                       |        |       ps.js
                                                                       |        |       pt-BR.js
                                                                       |        |       pt.js
                                                                       |        |       ro.js
                                                                       |        |       ru.js
                                                                       |        |       sk.js
                                                                       |        |       sl.js
                                                                       |        |       sq.js
                                                                       |        |       sr-Cyrl.js
                                                                       |        |       sr.js
                                                                       |        |       sv.js
                                                                       |        |       th.js
                                                                       |        |       tk.js
                                                                       |        |       tr.js
                                                                       |        |       uk.js
                                                                       |        |       vi.js
                                                                       |        |       zh-CN.js
                                                                       |        |       zh-TW.js
                                                                       |        |
                                                                       |        \--xregexp
                                                                       |             LICENSE.txt
                                                                       |             xregexp.js
                                                                       |             xregexp.min.js
                                                                       |
                                                                       +--http_response
                                                                       |  +--css
                                                                       |  |    alerts.css
                                                                       |  |    status.css
                                                                       |  |
                                                                       |  \--js
                                                                       |       alerts.js
                                                                       |
                                                                       \--scraper
                                                                          \--css
                                                                               style.css
``` -->

<!-- ![#f03c15](https://placehold.co/15x15/f03c15/f03c15.png) `#f03c15` -->
<!-- 
## Optimizations

- #### **Problem**: When you search something in search bar, n_videos will be added along with searchquery which has default value set by app setting 'MIN_SEARCH_VIDEOS' in database. suppose n_videos=5 then it will give 5 videos for that searchquery. Now I want to get more videos so I will change n_videos=10 within url, in that way it will also render those 5 video which allready rendered. It suppose to be render only 5 addition videos.


- #### **Possible solutions**
  option-1: storing response data in cookie\
  option-2: append response data by ajex


>\
>54889\
>54889\
>54889\
>54889




 -->
