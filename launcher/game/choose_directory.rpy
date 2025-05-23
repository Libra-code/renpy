﻿# Copyright 2004-2025 Tom Rothamel <pytom@bishoujo.us>
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

init python:

    try:
        import _renpytfd
    except Exception:
        _renpytfd = None

    def directory_is_writable(path):
        test = os.path.join(path, "renpy test do not use")

        try:
            if os.path.isdir(test):
                os.rmdir(test)

            os.mkdir(test)
            os.rmdir(test)

            return True

        except Exception:
            return False

    def choose_directory(default_path):
        """
        Pops up a directory chooser.

        `path`
            The directory that is selected by default. If None, config.renpy_base
            is selected.

        Returns a (path, is_default) tuple, where path is the chosen directory,
        and is_default is true if and only if it was chosen by default mechanism
        rather than user choice.
        """

        if _renpytfd:
            path = _renpytfd.selectFolderDialog(__("Select Projects Directory"), default_path)
        else:
            path = None

            if default_path is None:
                try:
                    default_path = os.path.dirname(os.path.abspath(config.renpy_base))
                except Exception:
                    default_path = os.path.abspath(config.renpy_base)

        # Path being None or "" means nothing was selected.
        if not path:

            if default_path is None or not os.path.isdir(default_path) or not directory_is_writable(default_path):
                interface.error(_("No directory was selected, but one is required."))

            return default_path, True

        # Apply more thorough checks to an explicit path.
        path = renpy.fsdecode(path)

        if not os.path.isdir(path):
            interface.error(_("The selected directory does not exist."))
        elif not directory_is_writable(path):
            interface.error(_("The selected directory is not writable."))

        return path, False
