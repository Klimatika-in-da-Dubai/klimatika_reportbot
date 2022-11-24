.PHONY: run clean

run:
	python main.py

setup: requirements.txt
	pip install -r requirements.txt
	pybabel extract --input-dirs=. -o locales/messages.pot
	pybabel init -i locales/messages.pot -d locales -D messages -l en
	pybabel compile -d locales -D messages

clean:
	rm -rf __pycache__
