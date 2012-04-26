# encoding: utf-8
"""
ncx.py

Created by Keith Fahlgren on Mon Jun 13 17:09:40 PDT 2011
Copyright (c) 2011 Threepress Consulting Inc. All rights reserved.
"""

import logging
import os.path

from lxml import etree

log = logging.getLogger(__name__)

NCX_TO_END = os.path.join(os.path.dirname(__file__), 'externals', 'xslt', 'ncx2end.xsl')
END_TO_NCX = os.path.join(os.path.dirname(__file__), 'externals', 'xslt', 'end2ncx.xsl')

def as_end(ncx):
    """Convert the supplied NCX document (as etree) to an EPUB (3) Navigation Document. Returns the 
       result as another etree document, ready for serialization.""" 
    end_transformer = etree.XSLT(etree.parse(NCX_TO_END))
    end = end_transformer(ncx)
    errors = end_transformer.error_log
    if str(errors).strip() != '':
        log.warn(errors)
    return end

def from_end(end):
    """Convert the supplied EPUB (3) Navigation Document (as etree) to an NCX document. Returns the 
       result as another etree document, ready for serialization.""" 
    ncx_transformer = etree.XSLT(etree.parse(END_TO_NCX))
    ncx = ncx_transformer(end)
    errors = ncx_transformer.error_log
    if str(errors).strip() != '':
        log.warn(errors)
    return ncx
