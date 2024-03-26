run:
	python -m streamlit run main.py
init: requirements.txt
	pip install -r requirements.txt
clean_db:
	rm databases/weather.db

