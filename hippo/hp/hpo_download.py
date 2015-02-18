import os
import os.path
import tempfile
import logging
import requests

__all__ = ["download_owl"]

logger = logging.getLogger(__name__)


def download_owl(url=None):
    filename = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "hp.owl"))
    if os.path.exists(filename) and os.path.getsize(filename) > 0:
        fd = open(filename, "rb")
        logger.info("Using cached file %s" % fd.name)
    else:
        try:
            fd = open(filename, "wb")
        except IOError:
            fd = tempfile.NamedTemporaryFile(suffix=".owl")
        logger.info("Downloading to %s..." % fd.name)
        _download_owl_fp(fd)
        fd.flush()
        fd.seek(0)

    return fd


def _download_owl_fp(outfile, url=None):
    url = url or "http://purl.obolibrary.org/obo/hp.owl"
    r = requests.get(url, stream=True)

    for chunk in r.iter_content(16000):
        outfile.write(chunk)
