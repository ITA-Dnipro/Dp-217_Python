# Dp-217_Python
Enrollment Assistant - a website that helps soon-to-be students find their way in life! The site provides surveys to help enrollees choose a path of education, and keeps track of universities and housing all over Ukraine to give a broader choice and help with relocation.

## Installation
The application can be downloaded through git:

    git clone https://github.com/ITA-Dnipro/Dp-217_Python.git

## Description

This is a multi-repo project, written (almost) entirely in python.
Set of used technologies and dependencies is different for every module. This readme aims at describing the main module of the application - Django Module. You can find specifications for other modules in their repos.
Other modules:
- [Parsing University Service](https://github.com/ITA-Dnipro/Dp-217_Python-parsing_university_service);
- [Parsing Relocation Service](https://github.com/ITA-Dnipro/Dp-217_Python-parsing_relocation_service);
- [Seeking Tickets Service](https://github.com/ITA-Dnipro/Dp-217_Python-ticket_seeker);
- [Mailing Service](https://github.com/ITA-Dnipro/Dp-217_Python-mailing).

### Structure & used technologies
The Django Module consists of Django back-end&front-end, PostgreSQL database and Nginx webserver.

The Django project is divided into 4 Django apps:
- [Users](#users);
- [Questioning](#questioning);
- [Universearch](#universearch);
- [Relocation](#relocation).

Used technologies: Docker, docker-compose, gettext, PostgreSQL, Nginx, CronTab

### Users
This app defines the user model and all user profile related funtions, including authorization.
The app contents can be found in the Dp-217_Python/users directory.

### Questioning
This app provides a survey system, that recommends dfferent education paths to a potential student based on a series of simple questions. It also contains definitions of survey-related models and a system that encodes survey results into an easy stored string, that can be decoded later.
The app contents can be found in the Dp-217_Python/questioning directory.

### Universearch
This app defines the university model, as well as related models like City, and provides an in-depth search system to filter out Universities by cities, available places, etc.
The app contents can be found in the Dp-217_Python/universearch directory.

### Relocation
This app defines the housing model. It also includes simple housing filters by city or university and is strongly dependant on the Universearch app.
The app contents can be found in the Dp-217_Python/relocation directory.

### Dependencies
These are python libraries listed in requirements.txt:
- Django==3.2.7
- django-crontab==0.7.1
- django-modeltranslation==0.17.3
- django-ckeditor==6.1.0
- djangorestframework==3.12.4
- Jinja2==3.0.2
- jinja2-time==0.2.0
- make==0.1.6.post2
- MarkupSafe==2.0.1
- psycopg2-binary==2.9.1
- requests==2.26.0
- kafka-python==2.0.2
- python-gettext==4.0

### Language
The interface of the application is multilingual (ua/ru/en). The source code contains comments, written in english.

## Credits
- [<img src="https://avatars.githubusercontent.com/u/83667809?v=4" width="16" height="16" />](https://github.com/artemmrgz) [@artemmrgz](https://github.com/artemmrgz)
- [<img src="https://avatars.githubusercontent.com/u/26443771?v=4" width="16" height="16" />](https://github.com/evroandrew) [@evroandrew](https://github.com/evroandrew)
- [<img src="https://avatars0.githubusercontent.com/u/49559296?s=460&v=4" width="16" height="16" />](https://github.com/gotoindex) [@gotoindex](https://github.com/gotoindex)
- [<img src="https://avatars.githubusercontent.com/u/72413229?v=4" width="16" height="16" />](https://github.com/maklabas) [@maklabas](https://github.com/maklabas)
- [<img src="https://avatars.githubusercontent.com/u/83273574?v=4" width="16" height="16" />](https://github.com/SerhiiTkachuk) [@SerhiiTkachuk](https://github.com/SerhiiTkachuk)
- [<img src="https://avatars.githubusercontent.com/u/28504014?v=4" width="16" height="16" />](https://github.com/suslovichb) [@suslovichb](https://github.com/suslovichb)
