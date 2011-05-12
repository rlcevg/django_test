export PYTHONPATH?=.
export DJANGO_SETTINGS_MODULE?=test_42cc.settings

IP?=127.0.0.1
PORT?=8000
APP?=contact

MANAGE=python test_42cc/manage.py

test: clean nosetests

nosetests:
	$(MANAGE) test $(APP)

clean:
	-find . -name '*.pyc' -exec rm -f {} \;
	-find . -name *~* -exec rm -f {} \;

run:
	$(MANAGE) runserver $(IP):$(PORT)
