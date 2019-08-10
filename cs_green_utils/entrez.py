# -*- coding: utf-8 -*-
"""entrez"""

import os
from time import sleep
from xml.etree import ElementTree

from cs_green_utils.http_k import get
from cs_green_utils.http_k import post


def _check_for_api_key():

    global_variables = globals()

    if 'ENTREZ_KEY' in global_variables:
        ncbi_api_key = global_variables['ENTREZ_KEY']
    elif 'ENTREZ_KEY' in os.environ:
        ncbi_api_key = os.environ['ENTREZ_KEY']
    else:
        print('Warning: ENTREZ_KEY is not defined.')
        ncbi_api_key = None

    return ncbi_api_key


ENTREZ_BASE_URL = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/'
DELAY = 1

def esearch(term, db, api_key=None):  # noqa

    if api_key is None:
        api_key = _check_for_api_key()

    eutil = 'esearch.fcgi'
    url = ENTREZ_BASE_URL + eutil

    params = {'db': db, 'term': term, 'idtype': 'acc', 'rettype': 'count',
              'retmode': 'json', 'usehistory': 'y', 'api_key': api_key}

    response = get(url, params, 'json')
    parsed = response.json()
    esearch_result = parsed['esearchresult']
    if 'ERROR' in esearch_result:
        raise Exception(esearch_result['ERROR'])

    record_count = int(esearch_result['count'])

    ret_max = 5000
    query_key = None
    web_env = None
    id_set = set()

    for ret_start in range(0, record_count, ret_max):

        if ret_start > 0:
            sleep(DELAY)

        params = {'db': db, 'term': term, 'idtype': 'acc',
                  'retstart': ret_start, 'retmax': ret_max,
                  'rettype': 'uilist', 'retmode': 'json', 'usehistory': 'y',
                  'api_key': api_key}

        if query_key is not None:
            params['query_key'] = query_key

        if web_env is not None:
            params['WebEnv'] = web_env

        response = get(url, params, 'json')
        parsed = response.json()
        data = parsed['esearchresult']

        id_set = id_set | set(data['idlist'])
        query_key = data['querykey']
        web_env = data['webenv']

    id_tuple = tuple(sorted(id_set))

    return_dict = {
        'db': db,
        'record_count': record_count,
        'ids': id_tuple,
        'query_key': query_key,
        'web_env': web_env}

    return return_dict


def epost(ids, db, api_key=None):  # noqa

    if api_key is None:
        api_key = _check_for_api_key()

    eutil = 'epost.fcgi'
    url = ENTREZ_BASE_URL + eutil
    data = {'db': db, 'id': ','.join(ids), 'api_key': api_key}

    response = post(url, data, 'xml')
    root = ElementTree.fromstring(response.text)

    query_key = None
    web_env = None

    for child in root:
        if child.tag == 'QueryKey':
            query_key = child.text
        if child.tag == 'WebEnv':
            web_env = child.text

    record_count = len(ids)

    return_dict = {
        'db': db,
        'record_count': record_count,
        'query_key': query_key,
        'web_env': web_env}

    return return_dict


def efetch_data(data, parser, ret_type=None, ret_mode='xml', api_key=None):  # noqa

    if api_key is None:
        api_key = _check_for_api_key()

    eutil = 'efetch.fcgi'
    url = ENTREZ_BASE_URL + eutil

    db = data['db']
    record_count = data['record_count']
    query_key = data['query_key']
    web_env = data['web_env']

    ret_max = 500
    ret_start = 0

    return_list = []

    for ret_start in range(0, record_count, ret_max):

        if ret_start > 0:
            sleep(DELAY)

        params = {'db': db, 'query_key': query_key, 'WebEnv': web_env,
                  'retstart': ret_start, 'retmax': ret_max,
                  'rettype': ret_type, 'retmode': ret_mode, 'usehistory': 'y',
                  'api_key': api_key}

        response = get(url, params, ret_mode)
        parsed = parser(response.text)

        for item in parsed:
            return_list.append(item)

    return return_list


def efetch(db, params, ret_type=None, ret_mode='xml', api_key=None):  # noqa

    if api_key is None:
        api_key = _check_for_api_key()

    eutil = 'efetch.fcgi'
    url = ENTREZ_BASE_URL + eutil

    params_all = {'db': db, 'rettype': ret_type, 'retmode': ret_mode,
                  'api_key': api_key}

    params_all.update(params)

    response = get(url, params_all, ret_mode)

    return response.text


def esummary(data, api_key=None):  # noqa

    if api_key is None:
        api_key = _check_for_api_key()

    eutil = 'esummary.fcgi'

    db = data['db']
    record_count = data['record_count']
    query_key = data['query_key']
    web_env = data['web_env']

    ret_max = 500

    return_list = []

    for ret_start in range(0, record_count, ret_max):

        if ret_start > 0:
            sleep(DELAY)

        url = ENTREZ_BASE_URL + eutil

        params = {'db': db, 'query_key': query_key, 'WebEnv': web_env,
                  'retstart': ret_start, 'retmax': ret_max, 'retmode': 'json'}

        response = get(url, params, 'json')
        parsed = response.json()['result']
        keys = parsed['uids']

        for k in keys:
            return_list.append(parsed[k])

    return return_list


def make_entrez_query(gene_names=[], nt_accs=[]):  # noqa

    gene_names = [gn + '[Gene Name]' for gn in gene_names]
    gene_names = ' OR '.join(gene_names)

    nt_accs = [ntacc + '[Nucleotide Accession]' for ntacc in nt_accs]
    nt_accs = ' OR '.join(nt_accs)

    query_elements = list()

    if gene_names != '':
        gene_names = '({})'.format(gene_names)
        query_elements.append(gene_names)

    if nt_accs != '':
        nt_accs = '({})'.format(nt_accs)
        query_elements.append(nt_accs)

    query = ' AND '.join(query_elements)

    return query
