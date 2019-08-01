PYTHON3		= python3
PIP		= python -m pip
NPM		= npm

VENV		= .venv
ACTIVATE	= . ${VENV}/bin/activate

LOCAL_SETTINGS  = charaViewer/local_settings.py
STATIC_ROOT	= static
DB_PATH		= db/db.sqlite3


.PHONY: usage
usage:
	@echo "${MAKE} targets"
	@echo ""
	@echo "Target:"
	@echo "  init             directory init"
	@echo "  build            less and JavaScript files build"
	@echo "  install          install static files"
	@echo "  clean            directory clean"

.PHONY: ${VENV}
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
	echo "STATIC_ROOT = ${STATIC_ROOT}" >> ${LOCAL_SETTINGS}
	echo "DB_PATH = ${DB_PATH}" >> ${LOCAL_SETTINGS}
	echo "VENV_SITE_DIR = `pwd`/`ls -d ${VENV}/lib/*/site-packages`" >> ${LOCAL_SETTINGS}

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
	${ACTIVATE} && python manage.py migrate

.PHONY: clean
clean:
	rm -rf node_modules
	rm -rf ${VENV}
	rm -rf ${LOCAL_SETTINGS}
