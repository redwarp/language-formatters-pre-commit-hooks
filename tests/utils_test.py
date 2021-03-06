# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import os
from os.path import basename

import mock
import pytest
from six.moves.urllib.parse import urljoin
from six.moves.urllib.request import pathname2url

from language_formatters_pre_commit_hooks.utils import download_url
from language_formatters_pre_commit_hooks.utils import run_command


@pytest.mark.parametrize(
    'command, expected_status, expected_output',
    [
        ['echo "1"', 0, '1\n'],
        ['echo "1" | grep 0', 1, ''],
        ['true', 0, ''],
        ['false', 1, ''],
    ],
)
def test_run_command(command, expected_status, expected_output):
    assert run_command(command) == (expected_status, expected_output)


@pytest.mark.parametrize(
    'url, does_file_already_exist',
    [
        [urljoin('file://', pathname2url(__file__)), True],
        [urljoin('file://', pathname2url(__file__)), False],
    ],
)
@mock.patch('language_formatters_pre_commit_hooks.utils.shutil', autospec=True)
@mock.patch('language_formatters_pre_commit_hooks.utils.requests', autospec=True)
def test_download_url(mock_requests, mock_shutil, tmpdir, url, does_file_already_exist):
    if does_file_already_exist:
        with open(os.path.join(tmpdir.strpath, basename(url)), 'w') as f:
            f.write('')

    with mock.patch.dict(os.environ, {'PRE_COMMIT_HOME': tmpdir.strpath}):
        assert download_url(url) == os.path.join(tmpdir.strpath, basename(url))

    if does_file_already_exist:
        assert not mock_requests.get.called
    else:
        mock_requests.get.assert_called_once_with(url, stream=True)
