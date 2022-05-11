APPNAME = yagv
VERSION = 0.5.8
# check setup.py and ./yagv too

all::
	@echo "make install deinstall"

install::
	python3 setup.py install
	sudo mkdir -p /usr/local/share/yagv;
	sudo tar cf - icon.png data | (cd /usr/local/share/yagv/; sudo tar xf -)
	cp yagv.desktop ~/.local/share/applications
	
deinstall::

# -- devs only:

edit::
	dee4 yagv gcodeParser.py Makefile tests/Makefile README.md setup.py

change::
	git commit -am "..."

push::
	git push origin master

pull::
	git pull

backup::
	cd ..; tar cfvz ~/Backup/${APPNAME}-${VERSION}.tar.gz ${APPNAME}; scp ~/Backup/${APPNAME}-${VERSION}.tar.gz backup:Backup/
