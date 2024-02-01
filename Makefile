PYTHON=python
TARGET=main.py
RM=rm -r
RM_TARGET=$(shell find ./ -name "__pycache__" -print)

.PHONY: run clean

run:
	$(PYTHON) $(TARGET)

setup: requirements.txt
	pip install -r requirements.txt
	pybabel compile -d locales -D messages

clean: SHELL:=/bin/bash
clean:
	for i in $(RM_TARGET) ; do \
		$(RM) $$i ; \
	done

update_po:
	pybabel extract --input-dirs=. -o locales/messages.pot
	pybabel update -d locales -D messages -i locales/messages.pot
	
compile_po:
	pybabel compile -d locales -D messages