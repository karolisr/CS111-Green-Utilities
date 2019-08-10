# -*- coding: utf-8 -*-
"""Entrez Workflows"""

from cs_green_utils.entrez import esearch, esummary, efetch
from cs_green_utils.entrez_parsers import genomic_info_from_es_result


def dnld_gene_gb_records(query, api_key=None):
    """
    Complete gene DNA

    Search genbank for genes that match the query. Extract the gene region
    from genomic DNA and return gb formatted records.
    """
    db_esearch = 'gene'
    db_efetch = 'nuccore'

    esearch_results = esearch(term=query, db=db_esearch, api_key=api_key)
    esummary_results = esummary(data=esearch_results, api_key=api_key)

    efetch_params_list = tuple(
        map(genomic_info_from_es_result, esummary_results))

    gb_records = list()

    for efetch_params in efetch_params_list:

        acc = efetch_params['id']
        beg = efetch_params['seq_start']
        end = efetch_params['seq_stop']
        strand = efetch_params['strand']
        orient = ''

        if strand == 2:
            orient = 'reversed and complemented'
            beg = efetch_params['seq_stop']
            end = efetch_params['seq_start']

        message = 'Downloading {}: {}..{} {}'.format(acc, beg, end, orient)
        print(message)

        efetch_results = efetch(db=db_efetch, params=efetch_params,
                                ret_type='gb', ret_mode='text',
                                api_key=api_key)

        tmp = efetch_results.split('\n\n')
        if len(tmp) > 1:
            tmp = tmp[:-1]
        else:
            continue

        gb_records = gb_records + tmp

    return gb_records
