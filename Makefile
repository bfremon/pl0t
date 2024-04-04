apt_install = /usr/bin/apt-get install
python3 = /usr/bin/python3
rm = /bin/rm -fr
rmdir = /bin/rmdir
git_pull = /usr/bin/git pull
git_log_url = https://github.com/bfremon/Log
venv_path = $(PWD)/venv
vpy = $(venv_path)/bin/python3
vpip = $(venv_path)/bin/pip3


packages = python3-pip

test: clean_test 
	. $(venv_path)/bin/activate && $(vpy) -m unittest discover

pip: venv README.md setup.py .VERSION LICENCE pl0t/__init__.py
	$(vpy) ./setup.py --set-build
	$(vpip) install .

clean: clean_test
	$(rm) __pycache__ pl0t/__pycache__  pl0t/tests/__pycache__ \
	venv/ Log/ pl0t.egg-info build/

venv: 
	@if [ ! -x venv ]; then \
		$(python3) -m venv $(venv_path); \
		. $(venv_path)/bin/activate; \
		$(vpy) -m pip install --upgrade pip setuptools wheel \
		seaborn scipy pandas numpy Log; \
		mkdir Log; cd Log; git init; \
		$(git_pull) $(git_log_url); \
		$(vpy) ./setup.py --set-build; \
		$(vpip) install . ; \
		$(rm) * .git .gitignore .VERSION; \
		cd .. ;\
		$(rmdir) $(PWD)/Log ;\
	else \
		echo 'Activating venv'; \
		. $(venv_path)/bin/activate; \
	fi;

clean_test:
	$(rm) *.svg *.png tmp/

.PHONY: pip clean test venv clean_test
