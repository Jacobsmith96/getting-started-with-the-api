#!/usr/bin/python
#
# Copyright 2014 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Python sample demonstrating use of the Google Genomics API.

Demonstrates:
  * Authorization flow
  * Using discovery to create the genomics/v1 service
  * Making calls to the genomics v1 service for reads and variants
"""

import argparse
from collections import Counter
from apiclient.discovery import build
import httplib2
from oauth2client import tools
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run_flow
from flask import Flask, render_template, request, jsonify, url_for, session, redirect
import json
from functools import wraps
from urllib import urlencode
import snps
import freq
import ga4gh
import requests
from snps import COORDINATES
from snps import DATA
import json

app = Flask(__name__)
SNP_TRANSLATION_FNAME = 'snps.sorted.txt.gz'
YEAR = 31536000
GENOTYPES = {snp: snp_data['Code'] for snp, snp_data in snps.DATA.iteritems()} 
REPOSITORIES = {
   'google': 'https://genomics.googleapis.com/v1',
   'ncbi': 'http://trace.ncbi.nlm.nih.gov/Traces/gg',
   'ebi': 'http://193.62.52.16',
   'ensembl': 'http://grch37.rest.ensembl.org/ga4gh'
}

# Authorization
storage = Storage('credentials.dat')
credentials = storage.get()
if credentials is None or credentials.invalid:
  flow = flow_from_clientsecrets(
      flags.client_secrets_filename,
      scope='https://www.googleapis.com/auth/genomics',
      message=('You need to copy a client_secrets.json file into this '
               'directory, or pass in the --client_secrets_filename option '
               'to specify where one exists. See the README for more help.'))
  credentials = run_flow(flow, storage, flags)

# Create a genomics API service
http = httplib2.Http()
http = credentials.authorize(http)
service = build('genomics', 'v1', http=http)

#
# This example gets the read bases for a sample at specific a position
#
@app.route('/')
def index():
    return render_template('index.html', sample_id='10473108253681171589')

def search_variants(genotypes, dataset, repo_id, callSetIds=None):
    '''
    yield genotypes within a dataset

    :param genotypes: dictionary mapping a variant name to a genotype
    :yield: GAVariant
    '''
    rsids_by_coords = {}
    rsids = set()
    for rsid in genotypes:
        rsids.add(rsid)
        coord = COORDINATES[rsid]
        chrom = coord['chromosome']
        end = coord['pos']
        start = end - 1
        rsids_by_coords['%s:%s-%s'% (chrom, start, end)] = rsid

    variantset_search_request = service.variantsets().search(
        body={'datasetIds':[dataset]},
        fields='variantSets(id)')

    variantset_search_resp=variantset_search_request.execute()

    variant_set_ids = []
    for vs in variantset_search_resp['variantSets']:
        variant_set_ids.append(vs['id'])
    vsid=variant_set_ids[0]
    maps = {}
    for vsid in variant_set_ids:
        for rsid in genotypes:
            request = service.variants().search(
            body={
                'variantSetIds': [vsid], 
                'referenceName': COORDINATES[rsid]['chromosome'],
                'start': COORDINATES[rsid]['pos']-1,
                'end': COORDINATES[rsid]['pos'] 
                },
            fields='variants(referenceName,start,end,referenceBases,alternateBases,calls)'
                )
            resp=request.execute()
            for variant in resp['variants']:    
                rsid = rsids_by_coords.get('%s:%s-%s'% (
                variant['referenceName'],
                variant['start'],
                variant['end']))
                if rsid is not None:
                    maps[rsid]=variant
                    print "rsid: " + rsid + ": Variant: "+ variant['referenceName']
    return maps.items()

@app.route('/snps/<sample_id>')
def get_snps(sample_id):
    dataset_id = '4252737135923902652' 
    sample = 'NA12546'
    reference_name = '7'

    # 1. First find the call set ID for the sample
    request = service.callsets().search(
        body={'variantSetIds': [dataset_id], 'name': sample},
        fields='callSets(id)')
    resp= request.execute()
    call_sets = resp.get('callSets', [])
    if len(call_sets) != 1:
        raise Exception('Searching for %s didn\'t return '
                  'the right number of call sets' % sample)

    call_set_id = call_sets[0]['id']
    
    print "Dataset ID: " + call_set_id
    print "Sample Name: " + sample
    print "Reference Name: " + reference_name

    variants = search_variants(
            GENOTYPES,
            dataset_id,
            callSetIds=[call_set_id],
            repo_id='google')

    snps = {}

    for rsid,variant in variants:
        gts = [variant['referenceBases']]
        gts.extend(variant['alternateBases']) 
        print gts
        for call in variant['calls']:
            if call.get('callSetId') != call_set_id:
                continue
            snps[rsid] = [gts[i] for i in call['genotype']]
    print "Finished loading snps."
    
    response = {}
    for rsid,variant in variants:
        gts = [variant['referenceBases']]
        gts.extend(variant['alternateBases']) 
        rsidentry = {}
        callentry = []
        rsidentry['referenceBases']=variant['referenceBases']
        rsidentry['alternateBases']=variant['alternateBases']
        for call in variant['calls']:
            if call.get('callSetId') != call_set_id:
                continue
            callentry=[gts[i] for i in call['genotype']]
        rsidentry['calls']=callentry
        rsidentry['start']=variant['start']
        rsidentry['end']=variant['end']
        response[rsid]=rsidentry
    finalResponse = {}
    finalResponse[sample]=response

    with open('data.txt', 'w') as outfile:
        json.dump(finalResponse, outfile)

    return jsonify(snps)

@app.route('/snp-data')
def get_snp_data():
    '''
    render SNPData.csv as json
    '''
    return jsonify(snps.DATA)

@app.route('/frequencies')
def get_frequencies():
    return jsonify(freq.FREQUENCIES) 

@app.route('/drug-info')
def get_drug_info():
    '''
    render DrugInfo.csv as json
    '''
    return jsonify(snps.DRUG_INFO) 

@app.route('/launch')
def launch():
    return render_template('launch.html')

if __name__ == '__main__':
    app.run(port=1028, debug=True, host='0.0.0.0')
