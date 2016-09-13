#!/usr/bin/env python3

import os.path
import unittest
from unittest.mock import call, MagicMock, mock_open, patch

import tacl
from .tacl_test_case import TaclTestCase


class CorpusTestCase (TaclTestCase):

    def setUp(self):
        self._tokenizer = tacl.Tokenizer(
            tacl.constants.TOKENIZER_PATTERN_CBETA,
            tacl.constants.TOKENIZER_JOINER_CBETA)

    def test_get_witness(self):
        Text = self._create_patch('tacl.corpus.WitnessText')
        path = '/test'
        name = 'foo'
        siglum = 'base'
        content = 'test content'
        filename = os.path.join(name, siglum + '.txt')
        m = mock_open(read_data=content)
        with patch('builtins.open', m, create=True):
            corpus = tacl.Corpus(path, self._tokenizer)
            actual_text = corpus.get_witness(name, siglum)
        m.assert_called_once_with(os.path.join(path, filename),
                                  encoding='utf-8')
        Text.assert_called_once_with(name, siglum, content, self._tokenizer)
        assert isinstance(actual_text, tacl.WitnessText)

    def test_get_witnesses(self):
        path = '/test'
        name1 = 'T1'
        name2 = 'T2'
        siglum1 = 'base'
        siglum2 = 'a'
        glob = self._create_patch('glob.glob')
        glob.return_value = [
            os.path.join(path, name1, siglum1 + '.txt'),
            os.path.join(path, name1, siglum2 + '.txt'),
            os.path.join(path, name2, siglum1 + '.txt')]
        isfile = self._create_patch('os.path.isfile')
        isfile.return_value = True
        get_witness = self._create_patch('tacl.Corpus.get_witness')
        get_witness.return_value = MagicMock(spec_set=tacl.WitnessText)
        corpus = tacl.Corpus(path, self._tokenizer)
        for text in corpus.get_witnesses():
            assert isinstance(text, tacl.WitnessText)
        glob.assert_called_once_with(os.path.join(path, '*/*.txt'))
        self.assertEqual(get_witness.mock_calls,
                         [call(corpus, name1, siglum1),
                          call(corpus, name1, siglum2),
                          call(corpus, name2, siglum1)])


if __name__ == '__main__':
    unittest.main()
