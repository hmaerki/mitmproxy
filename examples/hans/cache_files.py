"""
This script reflects all content passing through the proxy.
"""
import re
import os
import io
import zlib
import logging
import pathlib

import PIL.Image

from mitmproxy import http

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

cachedir = os.environ.get('MITMPROXY_CACHEDIR', './images_cache')
MITMPROXY_CACHEDIR = pathlib.Path(cachedir)
if not MITMPROXY_CACHEDIR.exists():
    MITMPROXY_CACHEDIR.mkdir()

REQUIRED_MINIMUM_SIZE_BYTES = 150*1000
REQUIRED_MINIMUM_WIDTHHEIGHT_PIXELS = 1500

class CacheFile:
    def __init__(self, flow):
        self.flow = flow
        content = self.__testIfRequired__()
        if content is None:
            return
        filename = self.__buildFilename__()
        directory = filename.parent
        if not directory.exists():
            directory.mkdir(parents=True)
        with open(filename, 'wb') as fOut:
            fOut.write(content)

    '''
    hallo.velo.ch => velo.ch
    velo.ch => velo.ch
    ch => Empty string (should never happen)
    Test with https://pythex.org
    '''
    reHostname = re.compile(r'([^\.]+\.[^\.]+)$')
    def __cutHostname(self, hostname):
        match = CacheFile.reHostname.search(hostname)
        assert match
        return match.group()

    def __buildFilename__(self):
        # 'luetzelsee.ch'
        hostname = self.flow.request.host
        hostname = self.__cutHostname(hostname)
        directory = MITMPROXY_CACHEDIR.joinpath(hostname)

        # 'thumbs/20110708_074924_pan.jpg'
        path = '/'.join(self.flow.request.path_components)

        filename = directory.joinpath(path)
        return filename.with_suffix('.jpg')

    def __testIfRequired__(self):
        contentType = self.flow.response.headers.get(b'content-type', None)
        if contentType != 'image/jpeg':
            return None
        content = self.flow.response.content
        contentEncoding = self.flow.response.headers.get(b'content-encoding', None)
        if contentEncoding is not None:
            assert contentEncoding == 'gzip'
            content = zlib.decompress(content, 16+zlib.MAX_WBITS)
        image = PIL.Image.open(io.BytesIO(content))
        width, height = image.size
        widthheight = width+height
        
        fSize = 100.0*len(content)/REQUIRED_MINIMUM_SIZE_BYTES
        fWidthHeight = 100.0*widthheight/REQUIRED_MINIMUM_WIDTHHEIGHT_PIXELS
        bTake = (fSize >= 100.0) | (fWidthHeight >= 100.0)

        msg = 'TAKE' if bTake else ' SKIP'
        logger.info(f'{msg}: {self.flow.request.url}: Size {fSize:0.0f}%%, width+height {fWidthHeight:0.0f}%%.')
        # if fSize >= 100.0:
        # print '%s: Bigger then %d bytes: %d' % (self.request.url.path, REQUIRED_MINIMUM_SIZE_BYTES, len(self.response.body))
        # return True
        # if fWidthHeight >= 100.0:
        # print '%s: Bigger then %d width+height: %d' % (self.request.url.path, REQUIRED_MINIMUM_WIDTHHEIGHT_PIXELS, width+height)
        # return True
        # print '%s: Small - skipped'
        if bTake:
            return content
        return None

def response(flow: http.HTTPFlow) -> None:
    # reflector = b"<style>body {transform: scaleX(-1);}</style></head>"
    # flow.response.content = flow.response.content.replace(b"</head>", reflector)

    try:
        c = CacheFile(flow)
    except Exception as e:
        print(e)
