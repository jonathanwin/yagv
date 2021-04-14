APPNAME = yagv
VERSION = 0.5.3
# check setup.py and ./yagv too

all::
	@echo "make install deinstall"

install::
	python3 setup.py install
	
deinstall::

# -- devs only:

edit::
	${EDITOR} yagv gcodeParser.py Makefile tests/Makefile README.md setup.py

change::
	git commit -am "..."

push::
	git push origin master

pull::
	git pull

backup::
	cd ..; tar cfvz ~/Backup/${APPNAME}-${VERSION}.tar.gz ${APPNAME}; scp ~/Backup/${APPNAME}-${VERSION}.tar.gz backup:Backup/
