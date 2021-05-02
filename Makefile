sudo = /usr/bin/sudo
apt_install = /usr/bin/apt-get install
python3 = /usr/bin/python3
rm = /bin/rm -fr
pip = /usr/bin/pip3

packages = python3-pip

test: clean
	$(python3) -m unittest discover

pip: README.md setup.py .VERSION LICENCE pl0t/__init__.py pre
	$(python3) ./setup.py --set-build
	$(pip) install .

clean:
	$(rm) __pycache__ pl0t/__pycache__  pl0t/tests/__pycache__ *.png *.svg 

pre:
	$(sudo) $(apt_install) python3-pip

.PHONY: pip clean test
