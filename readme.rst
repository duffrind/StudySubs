=====
StudySubs
=====

StudySubs is a simple Django app that allows the user to upload
subtitle files (or any file with Japanese text) and StudySubs will
tokenize the words, extract vocabulary words, conjugate them to
dictionary form (if needed), tag the word with part of speech,
get the English translation, and then output all of that information
into a CSV file which may be imported into Anki to study. The user
also has the options to download only new vocabulary words that he
or she may not know already, all the vocabulary words from the file,
and/or all previously seen vocabulary.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "subs" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
<<<<<<< HEAD
        'polls',
    ]/Users/duffrind/subtitles/studysubs/requirements.txt
=======
        'subs',
    ]
>>>>>>> f14b0c72f82e56296969ef66a71c881216efa0f1

2. Include the subs URLconf in your project urls.py like this::

    url(r'^subs/', include('subs.urls')),

3. Run `python manage.py migrate` to create the StudySubs models.

4. Start the development server and visit http://127.0.0.1:8000/admin/
   to view the database with all vocabulary (you'll need the Admin app enabled).

5. Visit http://127.0.0.1:8000/ to view the homepage.
