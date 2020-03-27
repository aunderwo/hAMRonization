#!/usr/bin/env python

import argparse
import csv
import json

from AntimicrobialResistance.Result import AntimicrobialResistanceResult

FIELD_MAP_NCBIAMRFINDERPLUS = {
    'protein_identifier': None,
    'contig_id': 'contig',
    'start': 'start',
    'stop': 'stop',
    'strand': 'strand_orientation',
    'gene_symbol': 'resistance_gene_symbol',
    'sequence_name': 'resistance_gene_name',
    'scope': None,
    'element_type': None,
    'element_subtype': None,
    'class': 'drug_class',
    'subclass': None,
    'method': None,
    'target_length': 'target_length',
    'reference_sequence_length': None,
    'percent_coverage_of_reference_sequence': 'coverage_percent',
    'percent_identity_of_reference_sequence': 'sequence_identity',
    'alignment_length': None,
    'accession_of_closest_sequence': 'reference_accession',
    'name_of_closest_sequence': None,
    'hmm_id': None,
    'hmm_description': None,
}

def parse_ncbi_amrfinderplus_report(path_to_ncbi_amrfinderplus_report):
    """
    Args:
        path_to_ncbi_amrfinderplus_report (str): Path to the NCBI AMRFinderPlus report file.
    
    Returns:
        list of dict: Parsed NCBI AMRFinderPlus report.
        For example:
        [
            {
                'protein_identifier': '',
                'contig_id': '',
                'start': '',
                'stop': '',
                'strand': '',
                'gene_symbol': '',
                'sequence_name': '',
                'scope': '',
                'element_type': '',
                'element_subtype': '',
                'class': '',
                'subclass': '',
                'method': '',
                'target_length': '',
                'reference_sequence_length': '',
                'percent_coverage_of_reference_sequence': '',
                'percent_identity_of_reference_sequence': '',
                'alignment_length': '',
                'accession_of_closest_sequence': '',
                'name_of_closest_sequence': '',
                'hmm_id': '',
                'hmm_description': '',
            },
            ...
        ]
    """
    ncbi_amrfinderplus_report_fieldnames = [
        'protein_identifier',
        'contig_id',
        'start',
        'stop',
        'strand',
        'gene_symbol',
        'sequence_name',
        'scope',
        'element_type',
        'element_subtype',
        'class',
        'subclass',
        'method',
        'target_length',
        'reference_sequence_length',
        'percent_coverage_of_reference_sequence',
        'percent_identity_of_reference_sequence',
        'alignment_length',
        'accession_of_closest_sequence',
        'name_of_closest_sequence',
        'hmm_id',
        'hmm_description',
    ]
    ncbi_amrfinderplus_report = []
    with open(path_to_ncbi_amrfinderplus_report) as ncbi_amrfinderplus_report_file:
        reader = csv.DictReader(ncbi_amrfinderplus_report_file, fieldnames=ncbi_amrfinderplus_report_fieldnames, delimiter='\t')
        next(reader) # skip header
        integer_fields = ['start', 'stop', 'target_length', 'reference_sequence_length', 'alignment_length']
        float_fields = ['percent_coverage_of_reference_sequence', 'percent_identity_of_reference_sequence']
        for row in reader:
            for key in integer_fields:
                row[key] = int(row[key])
            for key in float_fields:
                row[key] = float(row[key])
            ncbi_amrfinderplus_report.append(row)

    return ncbi_amrfinderplus_report


def prepare_for_amr_class(parsed_ncbi_amrfinderplus_report, additional_fields={}):
    input_for_amr_class = {}
    input_for_amr_class['analysis_software_name'] = "AMRFinderPlus"
    for key, value in additional_fields:
        input_for_amr_class[key] = value

    for ncbi_amrfinderplus_field, amr_result_field in FIELD_MAP_NCBIAMRFINDERPLUS.items():
        if amr_result_field:
            input_for_amr_class[str(amr_result_field)] = parsed_ncbi_amrfinderplus_report[str(ncbi_amrfinderplus_field)]

    return input_for_amr_class


def main(args):
    parsed_ncbi_amrfinderplus_report = parse_ncbi_amrfinderplus_report(args.ncbi_amrfinderplus_report)

    additional_fields = {}
    if args.analysis_software_version:
        additional_fields['analysis_software_version'] = args.analysis_software_version
    if args.database_version:
        additional_fields['database_version'] = args.database_version

    amr_results = []
    for result in parsed_ncbi_amrfinderplus_report:
        amr_class_input = prepare_for_amr_class(result, additional_fields)
        amr_result = AntimicrobialResistanceResult(amr_class_input)
        amr_results.append(amr_result)

    print(amr_results)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("ncbi_amrfinderplus_report", help="Input NCBI AMRFinderPlus report")
    parser.add_argument("--analysis_software_version", help="Version of NCBI AMRFinderPlus used to generate the report")
    parser.add_argument("--database_version", help="Version of NCBI AMRFinder database used to generate the report")
    args = parser.parse_args()
    main(args)
