# -*- coding: utf-8 -*-

""" Fields to help with common functionality, for example Upload fields with
``WTForms``.

Note
----
The following packages must be installed:

* Flask-WTF
"""

import calendar
import datetime
import ntpath
import os

from flask import current_app
from flask_wtf.file import FileField
from werkzeug import secure_filename
from werkzeug.datastructures import FileStorage


class UploadFileField(FileField):
    """ A django style upload field, allowing files to be uploaded and
    deleted when changed.

    Warning
    -------
    An application config variable called ``MEDIA_ROOT`` needs to be
    defined. This should be an absolute path to a directory to where
    uploaded files will be written.

    Example
    -------

    .. code-block:: python
        :linenos:

        from flask.ext.velox.fields import UploadFileField
        from flask_wtf import Form
        from flask_wtf.file import FileAllowed, FileRequired

        class MyForm(Form):
            name = UploadFileField('name', validators=[
                FileRequired(),
                FileAllowed(['pdf', ], 'PDF Only')])
    """

    # Deleting orphans relates to updating a record with a new file, the
    # existing attached file would become orphaned from its related record
    # delete_orphans ensures the existing file is removed if it has an
    # existing file attached to the obj
    delete_orphans = True

    def __init__(self, upload_to=None, *args, **kwargs):
        """ Overrides constructor method of `FileField` allowing
        `UploadFileField` to take extra arguments.

        Arguments
        ---------
        upload_to : str
            Relative path to upload files to
        """

        if upload_to:
            self.upload_to = upload_to

        return super(UploadFileField, self).__init__(*args, **kwargs)

    @property
    def absolute_dir_path(self):
        """ Returns the absolute path to the directory in which the file should
        be written too.

        Returns
        -------
        str
            Path to directory

        Raises
        ------
        NotImplementedError
            If ``MEDIA_ROOT`` is not defined in app config
        """

        config = current_app.config
        path = getattr(self, 'absolute_base', config.get('MEDIA_ROOT'))
        if not path:
            raise NotImplementedError(
                'Unable to get an absolute path to save files to, either '
                'define `absolute_base` or set `MEDIA_ROOT` app '
                'configuration value')

        # If upload_to is set join the base with the upload_to directory
        upload_to = getattr(self, 'upload_to', None)
        if upload_to:
            path = os.path.join(
                path,
                upload_to)

        return path

    @property
    def relative_dir_path(self):
        """ Returns the relative path of the directory, this is used for
        storing relative paths in a DB rather than absolute ones. By default
        this will be blank so the relative path for a file names `foo.jpg`
        would be `foo.jpg`

        Returns
        -------
        str
            Relative path to file
        """

        path = getattr(self, 'relative_base', '')

        # If upload_to is set join the base with the upload_to directory
        upload_to = getattr(self, 'upload_to', None)
        if upload_to:
            path = os.path.join(
                path,
                upload_to)

        return path

    def make_paths(self, obj):
        """ Returns built paths for saving to the file system, storing a
        relative path in a DB and the secure filename. In the case where the
        exact same filename exists in the same directory a UNIX timestamp is
        appended to the end of the filename to ensure no overwrites of existing
        files occure.

        Arguments
        ---------
        obj : obj
            The object being populated by the form

        Returns
        -------
        tuple
            Realtive path, Absolute path, filename
        """

        # Get filename
        filename = secure_filename(self.data.filename)

        absolute_path = os.path.join(
            self.absolute_dir_path,
            filename)

        if os.path.exists(absolute_path):
            # A File with the same name already exists in this dir
            # we will alter the filename to contain a timestamp of the upload
            # date of this file
            now = datetime.datetime.utcnow()
            timestamp = calendar.timegm(now.utctimetuple())
            name, ext = os.path.splitext(filename)

            # build filename
            filename = '{name}_{timestamp}{ext}'.format(
                name=name,
                timestamp=timestamp,
                ext=ext)

            # Reset absolute_path to use the new filename
            absolute_path = os.path.join(
                self.absolute_dir_path,
                filename)

        relative_path = os.path.join(
            self.relative_dir_path,
            filename)

        return absolute_path, relative_path, filename

    def populate_obj(self, obj, name):
        """ Called when populating an object such as a SQLAlchemy model with
        field data.

        In the case of `UploadFileField` this method will trigger the
        proceess of safely saving the file and setting the field data
        to be a relative path to the file.

        Arguments
        ---------
        obj : obj
            Instance of the object
        name : str
            Name of the field
        """

        if self.data and isinstance(self.data, FileStorage):
            absolute_path, relative_path, filename = self.make_paths(obj)
            self.save(absolute_path)

            if self.delete_orphans:
                origional_value = getattr(obj, name)
                if not origional_value is None \
                        and not origional_value == relative_path:
                    self.delete(origional_value)

            # Set field attribute to be value of the relative save path
            setattr(obj, name, relative_path)

    def delete(self, relative_path):
        """ Delete an existing file

        Arguments
        ---------
        relative : str
            The path to the saved the file to delete
        """

        # Give us just the filename from the relative path
        filename = ntpath.basename(relative_path)

        # Generate absolute path to file
        absolute_path = os.path.join(
            self.absolute_dir_path,
            filename)

        if os.path.exists(absolute_path):
            os.remove(absolute_path)

    def save(self, absolute_path):
        """ Save the file to the file system. In the event the destination
        directory does not exist it will attempt to create it.

        Arguments
        ---------
        absolute_path : str
            The path to save the file too
        """

        base = os.path.dirname(os.path.realpath(absolute_path))

        # If the absolute_base does not exist create it
        if not os.path.exists(base):
            os.makedirs(base)

        self.data.save(absolute_path)
