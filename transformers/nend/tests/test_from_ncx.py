#!/usr/bin/env python
# encoding: utf-8
'''
test_from_ncx.py

Created by Keith Fahlgren on Wed Apr 25 15:16:44 PDT 2012
Copyright (c) 2012 Safari Books Online. All rights reserved.
'''

import difflib
import glob
import logging
import os.path

from nose.tools import *

from lxml import etree


import nend
import nend.ncx


log = logging.getLogger(__name__)


class TestFromNCX(object):
    def setup(self):
        self.testfiles_dir = os.path.join(os.path.dirname(__file__), 'files')

    def test_end_ncx_output_same_smoke(self):
        '''An EPUB Navigation Document transformed to an NCX document should match the expected result'''
        for end_fn in glob.glob(self.testfiles_dir + '/expected*.html'):
            end_docname, _ = os.path.splitext(os.path.basename(end_fn))
            expected_ncx_fn = os.path.join(self.testfiles_dir, end_docname + '.ncx')
            expected_ncx = etree.parse(expected_ncx_fn)

            log.debug(end_fn)
            end = etree.parse(end_fn)
            ncx = nend.ncx.from_end(end)
            log.debug(etree.tostring(ncx))
            # Ensure the output is valid before testing the exact representation
            assert(nend.ncx_validate(ncx))
            try:
                assert_equal(etree.tostring(expected_ncx), etree.tostring(ncx))
            except AssertionError:
                try:
                    pretty_expected_ncx = etree.tostring(expected_ncx, pretty_print=True)
                    pretty_ncx = etree.tostring(ncx, pretty_print=True)
                    assert_equal(pretty_expected_ncx, pretty_ncx)
                except AssertionError:
                    # This is an absurd oneliner to keep the nose detailed-errors
                    # output small
                    diff = '\n'.join(list(difflib.unified_diff(pretty_expected_ncx.splitlines(),
                                                               pretty_ncx.splitlines())))
                    raise AssertionError('XML documents for %s did not match. Diff:\n%s' % (end_docname, diff))

    def test_ncx_nend_output_valid_smoke(self):
        '''All EPUB Navigation Documents collected for smoketesting should be able to be transformed into a valid NCX Document'''
        smoketests_dir = os.path.join(self.testfiles_dir, 'smoketests')
        for end_fn in glob.glob(smoketests_dir + '/*.html'):
            log.debug('\nSmoke testing transformation and validation of %s' % end_fn)
            end = etree.parse(end_fn)
            ncx = nend.ncx.from_end(end)
            assert(nend.ncx_validate(ncx))


