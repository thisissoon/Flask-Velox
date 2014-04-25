Change Log
==========

Next Release
------------
- Feature: ``ObjectView`` and ``ObjectMixin`` for rendering single objects
- Feature: ``request.view_args`` can now be accessed as view instance
  attributes for accessing in other methods
- Feature: Ability to customise context name for ``objects`` / ``object``
  within SQLAlchemy read views.

2014.04.24.2
------------
- Hotfix: Templates not included in MANIFEST.in resulting in missing from
  build.

2014.04.24.1
------------
- Hotfix: Fixed issue with ``BaseFormMixin`` where ``get_redirect_url_rule``
  would look for an incorrect attribute resulting in ``NotImplementedError``
  being risen.

Initial Release - 2014.04.24
----------------------------
- Initial release and feature set
