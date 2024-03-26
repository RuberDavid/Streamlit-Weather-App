run:
	python -m streamlit run main.py
init: requirements.txt
	pip install -r requirements.txt
get_dependencies:
	pip freeze > requirements.txt
clean_db:
	rm databases/weather.db

