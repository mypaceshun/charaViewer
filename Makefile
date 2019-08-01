PYTHON3		= python3
NPM		= npm

VENV		= .venv
ACTIVATE	= . ${VENV}/bin/activate

STATIC_ROOT	= static
DB_PATH		= db/db.sqlite3


.PHONY: usage
usage:
	@echo "${MAKE} targets"
	@echo ""
	@echo "Target:"
	@echo "  build            less and JavaScript files build"
	@echo "  install          install static files"

.PHONY: ${VENV}
${VENV}:
	${PYTHON3} -m venv ${VENV}
	${ACTIVATE} && pip install --upgrade pip wheel setuptools
	${ACTIVATE} && pip install -r requirements.txt
	touch ${VENV}

.PHONY: build
build:
	${NPM} run build

.PHONY: install
install: ${VENV}
	${MAKE} build
	${ACTIVATE} && \
	CHARAVIEWER_STATIC_ROOT=${STATIC_ROOT} \
	python manage.py collectstatic
	mkdir -p `dirname ${DB_PATH}`
	${ACTIVATE} && \
	CHARAVIEWER_DB_PATH=${DB_PATH} \
	python manage.py migrate
