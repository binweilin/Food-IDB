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
