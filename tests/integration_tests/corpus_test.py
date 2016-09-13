import os.path
import unittest

import tacl


class CorpusIntegrationTestCase (unittest.TestCase):

    def setUp(self):
        self._data_dir = os.path.join(os.path.dirname(__file__), 'data',
                                      'stripped')
        self._tokenizer = tacl.Tokenizer(
            tacl.constants.TOKENIZER_PATTERN_CBETA,
            tacl.constants.TOKENIZER_JOINER_CBETA)

    def test_get_sigla(self):
        corpus = tacl.Corpus(self._data_dir, self._tokenizer)
        actual_sigla = corpus.get_sigla('T1')
        expected_sigla = ['base', 'a']
        self.assertEqual(set(actual_sigla), set(expected_sigla))

    def test_get_witness(self):
        corpus = tacl.Corpus(self._data_dir, self._tokenizer)
        actual_text = corpus.get_witness('T1', 'base')
        expected_text = tacl.WitnessText('T1', 'base', 'then we went\n',
                                         self._tokenizer)
        self.assertEqual(actual_text.get_checksum(),
                         expected_text.get_checksum())
        self.assertEqual(actual_text.get_filename(),
                         expected_text.get_filename())

    def test_get_witnesses(self):
        corpus = tacl.Corpus(self._data_dir, self._tokenizer)
        expected_texts = [
            tacl.WitnessText('T1', 'a', 'the we went\n', self._tokenizer),
            tacl.WitnessText('T1', 'base', 'then we went\n', self._tokenizer),
            tacl.WitnessText('T2', 'a', 'thews he sent\n', self._tokenizer),
            tacl.WitnessText('T2', 'base', 'these he sent\n', self._tokenizer),
            tacl.WitnessText('T3', 'base', 'that\n', self._tokenizer),
            tacl.WitnessText('T4', 'base', 'hense\n', self._tokenizer),
            tacl.WitnessText('T5', 'base', 'well\n', self._tokenizer)]
        actual_texts = list(corpus.get_witnesses())
        actual_texts.sort(key=lambda x: x.get_filename())
        for actual_text, expected_text in zip(actual_texts, expected_texts):
            self.assertEqual(actual_text.get_filename(),
                             expected_text.get_filename())
            message = 'Checksum of {} does not match expected checksum from ' \
                      'supplied {}'.format(actual_text.get_filename(),
                                           expected_text.get_filename())
            self.assertEqual(actual_text.get_checksum(),
                             expected_text.get_checksum(), message)


if __name__ == '__main__':
    unittest.main()
