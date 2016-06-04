"""Command-line script to list texts from one sub-corpus (labelled set
of texts defined in a catalogue file) in order of similarity to each
text in that corpus. Takes into account a second sub-corpus of texts
that are similar to those in the first, but not in the way(s) that are
the subject of the investigation."""

import argparse
import logging
import os

import tacl
import tacl.command.utils as utils


logger = logging.getLogger('tacl')


def main ():
    parser = generate_parser()
    args = parser.parse_args()
    if hasattr(args, 'verbose'):
        utils.configure_logging(args.verbose, logger)
    store = utils.get_data_store(args)
    corpus = utils.get_corpus(args)
    catalogue = utils.get_catalogue(args.catalogue)
    tokenizer = utils.get_tokenizer(args)
    check_catalogue(catalogue, args.label)
    store.validate(corpus, catalogue)
    output_dir = os.path.abspath(args.output)
    if os.path.exists(output_dir):
        logger.warning('Output directory already exists; any results therein '
                       'will be reused rather than regenerated.')
    os.makedirs(output_dir, exist_ok=True)
    processor = tacl.JITCProcessor(store, corpus, catalogue, args.label,
                                   tokenizer, output_dir)
    processor.process()

def check_catalogue (catalogue, label):
    """Raise an exception if `catalogue` contains more than two labels, or
    if `label` is not used in the `catalogue`."""
    labels = set(catalogue.values())
    if label not in labels:
        raise Exception(
            'The specified label "{}" must be present in the catalogue.')
    elif len(labels) != 2:
        raise Exception('The catalogue must specify only two labels.')

def generate_parser ():
    parser = argparse.ArgumentParser(description='Generate a report showing the amount of overlap between a set of texts, ignoring those parts that overlap with texts in a second set of texts.')
    utils.add_common_arguments(parser)
    utils.add_db_arguments(parser)
    utils.add_corpus_arguments(parser)
    utils.add_query_arguments(parser)
    parser.add_argument('label', metavar='LABEL',
                        help='Label of texts to compare with each other')
    parser.add_argument('output', help='Directory to output results into',
                        metavar='OUTPUT')
    return parser
