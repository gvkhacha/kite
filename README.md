# Kite
**Kite** is an information retrieval system made as a part of a course at University of California Irvine offered to undergraduate students (CS 121). This system does not actually crawl the web, but indexes a corpus from [ics.uci.edu](http://ics.uci.edu) containing approximately 37,000 documents. 

Virtual environment (pipenv) used for Python3, BeautifulSoup, lxml, nltk and Django (UI). 3-step process to building and querying index shown below.


# Parsing & Building Index

Kite searches through *bookkeeping.json* to find local directories to raw files as well as the URL in which it was downloaded from. Raw files are opened, parsed with the help of [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) and tokenized to a inverted index in the form of {token: (docID, weight)}

    python build_index.py -r   # Backs up dictionary and restarts with empty ones
    python build_index.py      # Continues parsing from first unread document

## Optimizing Index

Finally opted to use database instead of raw files, using sqlite (even though relational database wasn't best option). In this conversion also computes tf-idf.

    python optimize_index.py


# Django User-Interface

User-interface isn't pretty, and extra features such as spell check and math have been excluded for the course.

    cd kite
    python manage.py runserver


