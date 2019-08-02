PYTHON3		= python3
PIP		= python -m pip
NPM		= npm

VENV		= .venv
ACTIVATE	= . ${VENV}/bin/activate

LOCAL_SETTINGS  = charaViewer/local_settings.py
STATIC_ROOT	= $(shell python3 -c "from charaViewer.local_settings import STATIC_ROOT; print(STATIC_ROOT)")
DB_PATH		= $(shell python3 -c "from charaViewer.local_settings import DB_PATH; print(DB_PATH)")

APACHE_GROUP    = www-data


.PHONY: usage
usage:
	@echo "${MAKE} targets"
	@echo ""
	@echo "Target:"
	@echo "  init             directory init"
	@echo "  build            less and JavaScript files build"
	@echo "  install          install static files"
	@echo "  clean            directory clean"

${VENV}:
	${PYTHON3} -m venv ${VENV}
	${ACTIVATE} && ${PIP} install --upgrade pip wheel setuptools
	${ACTIVATE} && ${PIP} install -r requirements.txt
	touch ${VENV}

.PHONY:init
init:
	${MAKE} ${VENV}
	${MAKE} ${LOCAL_SETTINGS}

${LOCAL_SETTINGS}:
	echo "DEBUG = False" > ${LOCAL_SETTINGS}
	echo "STATIC_ROOT = 'static'" >> ${LOCAL_SETTINGS}
	echo "DB_PATH = 'db.sqlite3'" >> ${LOCAL_SETTINGS}
	echo "VENV_SITE_DIR = '`pwd`/`ls -d ${VENV}/lib/*/site-packages`'" >> ${LOCAL_SETTINGS}

node_modules: package.json
	${NPM} install

.PHONY: build
build: node_modules
	${NPM} run build

.PHONY: install
install:
	${MAKE} init
	${MAKE} build
	${ACTIVATE} && python manage.py collectstatic
	mkdir -p `dirname ${DB_PATH}`
	chgrp ${APACHE_GROUP} `dirname ${DB_PATH}`
	chmod g+w `dirname ${DB_PATH}`
	${ACTIVATE} && python manage.py migrate

.PHONY: clean
clean:
	rm -rf node_modules
	rm -rf ${VENV}
	rm -rf ${LOCAL_SETTINGS}
