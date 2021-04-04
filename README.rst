=====================
Py Bipartite Matching
=====================
.. image:: https://raw.githubusercontent.com/FranciscoMoretti/py_bipartite_matching/master/icon_152x200.png
        :height: 200px
        :align: center
        :alt: Bipartite graph

.. image:: https://img.shields.io/pypi/v/py_bipartite_matching.svg
        :target: https://pypi.python.org/pypi/py_bipartite_matching

.. image:: https://pyup.io/repos/github/FranciscoMoretti/py_bipartite_matching/shield.svg
     :target: https://pyup.io/repos/github/FranciscoMoretti/py_bipartite_matching/
     :alt: Updates

.. image:: https://travis-ci.com/FranciscoMoretti/py_bipartite_matching.svg?branch=master
    :target: https://travis-ci.com/FranciscoMoretti/py_bipartite_matching

.. image:: https://readthedocs.org/projects/py-bipartite-matching/badge/?version=latest
        :target: https://py-bipartite-matching.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status



Algorithms for Enumerating All Perfect, Maximum and Maximal Matchings in Bipartite Graphs.

Algorithm described in "Algorithms for Enumerating All Perfect, Maximum and Maximal Matchings in Bipartite Graphs"
By Takeaki Uno in "Algorithms and Computation: 8th International Symposium, ISAAC '97 Singapore,
December 17-19, 1997 Proceedings"
See http://dx.doi.org/10.1007/3-540-63890-3_11

* Free software: MIT license
* Documentation: https://py-bipartite-matching.readthedocs.io.


Features
--------

* Functions available:
        * enum_perfect_matchings
        * enum_maximum_matchings

usage
-----

To use Py Bipartite Matching in a project the `networkx` package is needed as well

.. code-block:: python

    import py_bipartite_matching as pbm
    import networkx as nx

Use ``enum_perfect_matchings`` to enumerate all perfect matchings

.. code-block:: python

    n = 2
    graph = nx.complete_bipartite_graph(n, n, nx.Graph)
    for matching in pbm.enum_perfect_matchings(graph):
        print(matching)

Output:

        {0: 2, 1: 3}
        
        {0: 3, 1: 2}

Use ``enum_maximum_matchings`` to enumerate all maximum matchings

.. code-block:: python

    n = 2
    m = 3
    graph = nx.complete_bipartite_graph(n, m, nx.Graph)
    for matching in enum_maximum_matchings(graph):
        print(matching)

Output:
       
        {0: 3, 1: 4}

        {0: 4, 1: 3}
        
        {0: 3, 2: 4}
        
        {1: 3, 2: 4}

        {0: 4, 2: 3}
        
        {2: 3, 1: 4}

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
