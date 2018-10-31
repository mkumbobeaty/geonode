How to use the API
==================

Request the full list::

    http://localhost:8000/wfpdocs/api/v1/?format=json

Request the full documents list::

    http://localhost:8000/wfpdocs/api/v1/wfp-document/?format=json

Request just one document (id=1)::

    http://localhost:8000/wfpdocs/api/v1/wfp-document/1/?format=json
    
Request document schema::

    http://localhost:8000/wfpdocs/api/v1/wfp-document/schema/?format=json
    
Request the a set of documents (id=1 and id=3)::

    http://localhost:8000/wfpdocs/api/v1/wfp-document/set/1;3/?format=json
    
Request documents for a given title::

    http://localhost:8000/wfpdocs/api/v1/wfp-document/?format=json&document__title=Test
    
Request documents newer than a certain date::

    http://localhost:8000/wfpdocs/api/v1/wfp-document/?format=json&document__date__gte=2013-12-12
    
Request documents for a certain category::

    http://localhost:8000/wfpdocs/api/v1/wfp-document/?format=json&categories__name=Emergency
    
Request documents for certain categories and newer than a certain date::

    http://localhost:8000/wfpdocs/api/v1/wfp-document/?format=json&categories__name__in=Emergency,Earthquake&document__date__gte=2013-12-12
    
Full reference for query syntax::

    https://docs.djangoproject.com/en/dev/topics/db/queries/
