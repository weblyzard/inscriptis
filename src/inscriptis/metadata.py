"""Inscriptis metadata information."""

import importlib.metadata as metadata

PACKAGE = "inscriptis"

__author__ = "Albert Weichselbraun, Fabian Odoni"
__author_email__ = "albert.weichselbraun@fhgr.ch, fabian.odoni@fhgr.ch"
__copyright__ = (
    f"{metadata.metadata(PACKAGE)['Name']} " + f"{metadata.metadata(PACKAGE)['Version']} © 2016-2025 {__author__}"
)
__license__ = metadata.metadata(PACKAGE)["License-Expression"]
__version__ = metadata.metadata(PACKAGE)["Version"]
