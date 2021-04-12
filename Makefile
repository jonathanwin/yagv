APPNAME = yagv
VERSION = 0.5.1

all::
	@echo "make install deinstall"

install::
	python3 setup.py install
	
deinstall::

# -- devs only:

edit::
	${EDITOR} yagv gcodeParser.py Makefile README.md setup.py

change::
	git commit -am "..."

push::
	git push origin master

pull::
	git pull

backup::
	cd ..; tar cfvz ~/Backup/${APPNAME}-${VERSION}.tar.gz ${APPNAME}; scp ~/Backup/${APPNAME}-${VERSION}.tar.gz backup:Backup/
