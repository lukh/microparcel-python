==================
microparcel-python
==================


.. image:: https://img.shields.io/pypi/v/microparcel.svg
        :target: https://pypi.python.org/pypi/microparcel

.. image:: https://img.shields.io/travis/lukh/microparcel-python.svg
        :target: https://travis-ci.org/lukh/microparcel-python

.. image:: https://readthedocs.org/projects/microparcel-python/badge/?version=latest
        :target: https://microparcel-python.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status



Serialize and deserialize structured data.

microparcel impementation in Python.

* Free software: MIT license


Provides three differents entities:

A Message is the payload, with methods to access specifics bitfields on the data buffer

The Frame encapsulates the Message between a Start Of Frame and a CheckSum

And the Parser is used to Parse bytes into Message and encodes Messages in Frame

See Documentation: https://microparcel-python.readthedocs.io/en/latest/

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
