# djinni-data-analysis
Service for parsing and analyzing data about the most popular technologies Python Developers on djinni.co

## How to run

```
git clone https://github.com/mdubyna/djinni-data-analysis.git
cd .\djinni-data-analysis\
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd app
python main.py
```

## Features

- saving parsing results in csv file
- analytics of the most popular technologies
- keyword filtering using nltk
- request processing in asynchronous mode