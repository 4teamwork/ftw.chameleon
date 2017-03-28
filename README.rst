.. contents:: Table of Contents


Introduction
============

This package enhances the integration of `Chameleon`_ into Plone with `five.pt`_.

In our deployments we have source checkouts (git) which we are pulled on updates.
This may cause templates to be updated on the next request in running instances,
which may cause errors because the associated code was not yet reloaded because
the zope instance was not yet rebooted.
In order to make that more robust we use `Chameleon`_ with eager-loading enabled
and auto-reload disabled, so that after an instance is started it will no longer
read templates.

These options do not work as expected when using `five.pt`_ for integrating
`Chameleon`_ in combination with ``ViewPageTemplateFile`` instances.
``ftw.chameleon`` contains enhancements for making that work well.


Enhancements
=============

- ``zope.pagetemplate`` is patched so that it considers the ``CHAMELEON_RELOAD``
  configuration: when ``CHAMELEON_RELOAD`` is disabled it does not trigger a
  recooking of the template even when it has changed.

- When ``CHAMELEON_EAGER`` is enabled, all templates will be cooked on startup.
  This is done by explicitly cooking all known templates in a separate thread.

- Fire an event when chameleon compiles templates.

- Log warnings or exceptions when templates are compiled unexpectedly.
  This helps to pin-point problems with templates which are not cacheable.

- When ``CHAMELEON_EAGER`` is enabled, the templates in ``portal_skins`` will be
  cooked after the first request on the Plone site.


Compatibility
=============

Plone 4.3.x


Installation
============

Buildout example for **production**:

.. code:: ini

    [instance]
    eggs +=
        ftw.chameleon
    environment-vars +=
        CHAMELEON_EAGER true
        CHAMELEON_RELOAD false
        CHAMELEON_CACHE ${buildout:directory}/var/chameleon-cache
        FTW_CHAMELEON_RECOOK_WARNING true

Buildout example for **development**:

.. code:: ini

    [instance]
    eggs +=
        ftw.chameleon
    environment-vars +=
        CHAMELEON_RELOAD true
        CHAMELEON_CACHE ${buildout:directory}/var/chameleon-cache


You need to make sure that the cache-directory exists. This can be done with buildout:

.. code:: ini

    [buildout]
    parts += chameleon-cache

    [chameleon-cache]
    directory = ${buildout:directory}/var/chameleon-cache
    recipe = collective.recipe.shelloutput
    commands =
        cmd1 = mkdir -p ${chameleon-cache:directory}

    [instance]
    environment-vars +=
        CHAMELEON_CACHE ${chameleon-cache:directory}



Environment variables
=====================

+-----------------------------------+-------------------------------------------+-------------------------+-----------------------------+
| **Name**                          | **Description**                           | **Values**              | **Recommendation**          |
+-----------------------------------+-------------------------------------------+-------------------------+-----------------------------+
| ``CHAMELEON_EAGER``               | Parse and compile templates on startup.   | ``true``, ``false``     |``true``                     |
+-----------------------------------+-------------------------------------------+-------------------------+-----------------------------+
| ``CHAMELEON_RELOAD``              | Reload templates when they have changed.  | ``true``, ``false``     |  ``false``                  |
+-----------------------------------+-------------------------------------------+-------------------------+-----------------------------+
| ``CHAMELEON_CACHE``               | File system cache.                        | Path to cache directory.| ``.../var/chameleon-cache`` |
+-----------------------------------+-------------------------------------------+-------------------------+-----------------------------+
| ``FTW_CHAMELEON_RECOOK_WARNING``  | Warn when recooking templates.            | ``true``, ``false``     | ``true``                    |
+-----------------------------------+-------------------------------------------+-------------------------+-----------------------------+
| ``FTW_CHAMELEON_RECOOK_EXCEPTION``| Exception when recooking templates.       | ``true``, ``false``     | ``true`` when using Sentry. |
+-----------------------------------+-------------------------------------------+-------------------------+-----------------------------+

See also the `Chameleon documentation <https://chameleon.readthedocs.io/en/latest/configuration.html>`_.



Development
===========

1. Fork this repo
2. Clone your fork
3. Shell: ``ln -s development.cfg buildout.cfg``
4. Shell: ``python bootstrap.py``
5. Shell: ``bin/buildout``

Run ``bin/test`` to test your changes.

Or start an instance by running ``bin/instance fg``.


Links
=====

- Github: https://github.com/4teamwork/ftw.chameleon
- Issues: https://github.com/4teamwork/ftw.chameleon/issues
- Pypi: http://pypi.python.org/pypi/ftw.chameleon


Copyright
=========

This package is copyright by `4teamwork <http://www.4teamwork.ch/>`_.

``ftw.chameleon`` is licensed under GNU General Public License, version 2.

.. _Chameleon: https://pypi.python.org/pypi/Chameleon
.. _five.pt: https://pypi.python.org/pypi/five.pt
