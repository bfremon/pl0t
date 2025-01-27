
rm = rm -fr
py = /usr/bin/python3
cp = /bin/cp
sudo = /usr/bin/sudo  
apt = $(sudo) /usr/bin/apt-get install
vpy = venv/bin/python3
vpip3 = venv/bin/pip3

deb_pkgs = dh-python python3-stdeb python3-virtualenv

test:
	$(py) -m unittest discover


pre: clean
	${apt} ${deb_pkgs}
	${MAKE} venv
	echo ${PWD}
	${vpip3} install -r requirements.txt


deb: whl venv setup.py
	$(py) setup.py --command-packages=stdeb.command \
	bdist_deb
	$(cp) deb_dist/*.deb .


whl: pre venv setup.py
	$(vpy) -m build .
	${cp} dist/*.whl .

venv:
	virtualenv venv
	. ./venv/bin/activate


.PHONY: clean whl venv deb


clean:
	$(rm) *.tar.gz *.egg-info dist/ deb_dist/ \
	*.deb *.whl venv/ build/
