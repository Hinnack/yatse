#!/usr/bin/env bash

VERSION=$(sed 's/\..*//' /etc/debian_version)

apt-get update
# debian packages
apt-get install -y locales-all screen gettext memcached python-memcache locales-all libjpeg62-turbo libjpeg-dev libpng-dev screen apache2 apache2-mpm-prefork libapache2-mod-wsgi python-dev sqlite3 gettext ant ntp
wget https://bootstrap.pypa.io/get-pip.py
python get-pip.py

# python modules
sites=`python -c "from distutils.sysconfig import get_python_lib; print get_python_lib()"`
ln -fs /vagrant_modules/yatse $sites 2>/dev/null
ln -fs /vagrant_modules/bootstrap_toolkit $sites 2>/dev/null

pip install -r /vagrant/requirements.txt

# yatse web
mkdir -p /var/web/yatse
ln -fs /vagrant_sites/static /var/web/yatse/static
mkdir -p /var/web/yatse/static
ln -fs /vagrant_sites/web /var/web/yatse/web

mkdir -p /var/web/yatse/logs
touch /var/web/yatse/logs/django_request.log
chown root:vagrant /var/web/yatse/logs/django_request.log
chmod go+w /var/web/yatse/logs/django_request.log

# yatse config
mkdir -p /usr/local/yatse/config
ln -fs /vagrant/web.ini /usr/local/yatse/config/web.ini

# yats db
mkdir -p /var/web/yatse/db
chown root:vagrant /var/web/yatse/db
chmod go+w /var/web/yatse/db

cd /var/web/yatse/web/
python manage.py migrate
python manage.py createsuperuser --username root --email root@localhost --noinput
python manage.py loaddata /vagrant/init_db.json
python manage.py collectstatic  -l --noinput

chown root:vagrant /var/web/yatse/db/yatse2.sqlite
chmod go+w /var/web/yatse/db/yatse2.sqlite

# apache config
cp /vagrant/yatse.apache /etc/apache2/sites-available/yatse.conf
a2dissite default
a2dissite 000-default
a2ensite yatse
apache2ctl restart

# deb upgrade
apt-get -y upgrade &

# running ant and ignore error
cd /vagrant_project
ant ci18n

timedatectl set-ntp true

echo "open http://192.168.33.17 with user: admin password: admin"
