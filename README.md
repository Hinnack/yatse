# yatse

[![license](https://img.shields.io/github/license/mediafactory/yats.svg)]()
[![GitHub issues](https://img.shields.io/github/issues/mediafactory/yats.svg)]()
[![GitHub pull requests](https://img.shields.io/github/issues-pr/mediafactory/yats.svg)]()
[![GitHub contributors](https://img.shields.io/github/contributors/mediafactory/yats.svg)]()
[![GitHub forks](https://img.shields.io/github/forks/mediafactory/yats.svg?style=social&label=Fork)]()
[![GitHub stars](https://img.shields.io/github/stars/mediafactory/yats.svg?style=social&label=Stars)]()

- combining more than one YATS (https://github.com/mediafactory/yats) in one interface and aggregate tickets together.
- &copy; media factory, Lübeck, Germany https://www.mediafactory.de
- requires: Django 1.11.x (Python 2.x)

DEMO
-----
use vagrant!

VAGRANT
-----
howto:
```
$ cd vagrant
$ vagrant up
```
Wait! :-)
Point your browser at:
http://192.168.33.17
or for admin interface:
http://192.168.33.17/admin

Staff User:  
Login: admin  
Password: admin

WHY?
-----
Having multiple YATS Installations for different projects make you loose the focus and hassle with different websites.

KEY FEATURES
-----
- all features from YATS still available in each installation
- SSO (single-sign-on) just on login for all
- still local login possible for customers
- search over all YATS-server
- Reports over all YATS-server
- Boards over all YATS-server
- view and change in each YATS local itself

INSTALLATION
-----
no pypi package yet!

There is a debian package which includes parts of all, but is very special designed for our usecase as we make no use of pip. It distributes all packages not available via debian packages.

settings.py reads part of its config data from an inifile (see top of settings.py).

The project is splited into 2 parts:
- the app (yatse)
- the web, using the app (web)
