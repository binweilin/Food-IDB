ls
s
ls
cd foodsite/
ls
cd foodsite/library/
ls
cd 
ls
ls -a
git add foodsite/foodsite/library/*
git status
git commit -am "Added some files necessary for django"
git push
exit
ls
git status
git commit foodsite/static/*
git add foodsite/static/*
git add *
git status
git commit -am "Added some stuff for models, added a few more html pages"
git push
exit
ls
cd foodsite/
ls
python3 manage.py shell
python3 manage.py test
ls
cd ..
ls
git pull
git commit -am "Completed 9 unit tests, fixes issue #2, fixes issue #3"
git status
git push
exit
ls
ls -a
git pull
git commit -am "Added some unit tests"
git push
ls
git status
git add *
git commit -m "site done again"
git push -u origin master
ls
cd foodsite/foodsite/library/
ls
python3 manage.py
ls
cd ../../
ls
python3 manage.py
python3 manage.py shell
ls
cd foodsite/library/
ls
pydoc -w models
git status
git commit -am "Changed some glyphicons, added to about page"
git push
git pull
git status
git pull
git commit -am "Changed some glyphicons, added to about page"
git push
ls
exit
cd foodsite/library/
ls
pydoc -w models
exit
ls
pip3.3 install --user https://dev.mysql.com/get/Downloads/Connector-Python/mysql-connector-python-1.1.6.tar.gz
pip3.3 install --user https://github.com/davispuh/MySQL-for-Python-3/archive/1.0.tar.gz
ls
./manage.py syncdb
python manage.py sql library
python manage.py sql foodsite
python3 manage.py sql foodsite
python3 manage.py sql library

python3 manage.py sql library
./manage.py syncdb
python3 manage.py sql library
from foodsite.library.models import Region
from foodsite.foodsite.library.models import Region
ls
from library.models import Region
python3
cd foodsite/
ls
from library.models import Region
python3
exit
python3 manage.py syncdb
use regionalfoods$default
mysql
./mysql
mysql shell
exit
ls
cd foodsite
python3 manage.py runserver
ls
python3 manage.py syncdb
python manage.py syncdb
exit
ls
cd foodsite/
l
ls
./manage.py test
cd foodsite/
ls
cd library/
ls
./tests
python3 tests.py
cd ../../
ls
python3 manage.py
./manage.py
python3
./manage.py shell
ls
python3 manage.py test --keepdb
python3 manage.py --keepdb test
./manage.py test --keepdb
./manage.py --keepdb test
ls
cd ..
git pull
exit
ls
cd foodsite/
ls
test.out
vim test.out 
ls
./manage.py test
./manage.py shell
python3 foodsite/library/tests.py
python3 tests.py
python3 library/tests.py
python3 foodsite.library/tests.py
python3 foodsite/library/tests.py
./manage.py shell
python3 foodsite/library/tests.py
./manage.py shell
coverage3 shell
coverage3
./manage.py shell
ls
cd
ls
ls -a
git pull
git add*
git add *
git commit -am "Implemented API and added API tests"
git commit -am "Implemented API and added API tests, fixes #24, fixes #26"
git push
pip install django-haystack
pwd
cd ..
lx
ls -l
cd ..
ls -l
cd home/regionalfoods/
sudo pip install django-haystack
cd ../
ls
virtualenv env
