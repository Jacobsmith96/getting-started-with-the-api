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

app = Flask(__name__)
SNP_TRANSLATION_FNAME = 'snps.sorted.txt.gz'
YEAR = 31536000
GENOTYPES = {snp: snp_data['Code'] for snp, snp_data in snps.DATA.iteritems()} 

'''
# For these examples, the client id and client secret are command-line arguments
parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter,
    parents=[tools.argparser])
parser.add_argument('--client_secrets_filename',
                    default='client_secrets.json',
                    help=('The filename of a client_secrets.json file from a '
                          'Google "Client ID for native application" that '
                          'has the Genomics API enabled.'))
flags = parser.parse_args()
'''
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

@app.route('/snps/<sample_id>')
def get_snps(sample_id):
    dataset_id = '10473108253681171589' 
    sample = 'NA12749'
    reference_name = '22'
    reference_position = 51003835

    # 1. First find the call set ID for the sample
    request = service.callsets().search(
        body={'variantSetIds': [dataset_id], 'name': sample},
        fields='callSets(id)')
    resp = request.execute()
    call_sets = resp.get('callSets', [])
    if len(call_sets) != 1:
        raise Exception('Searching for %s didn\'t return '
                  'the right number of call sets' % sample)

    call_set_id = call_sets[0]['id']
    print call_set_id
    # 2. Once we have the call set ID,
    # lookup the variants that overlap the position we are interested in
    # request = service.variants().search(
    #     body={'callSetIds': [call_set_id],
    #           'referenceName': reference_name,
    #         'start': reference_position,
    #         'end': reference_position + 1},
    #     fields='variants(names,referenceBases,alternateBases,calls(genotype))')
    # variants = request.execute()
    # variant = request.execute().get('variants', [])[0]

    # variant_name = variant['names'][0]
    # genotype = [variant['referenceBases'] if g == 0
    #         else variant['alternateBases'][g - 1]
    #         for g in variant['calls'][0]['genotype']]

    # print 'the called genotype is %s for %s' % (','.join(genotype), variant_name)
    print GENOTYPES
    variants = ga4gh.search_variants(
            GENOTYPES,
            dataset_id,
            callSetIds=[call_set_id],
            repo_id='google')
    snps = {}

    for rsid,variant in variants:
        gts = [variant['referenceBases']]
        gts.extend(variant['alternateBases']) 
        for call in variant['calls']:
            if call.get('callSetId') != call_set_id:
                continue
            snps[rsid] = [gts[i] for i in call['genotype']]
    print "finished loading snps"
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
#
# This example gets the variants for a sample at a specific position
#
'''
# 1. First find the call set ID for the sample
request = service.callsets().search(
    body={'variantSetIds': [dataset_id], 'name': sample},
    fields='callSets(id)')
resp = request.execute()
call_sets = resp.get('callSets', [])
if len(call_sets) != 1:
  raise Exception('Searching for %s didn\'t return '
                  'the right number of call sets' % sample)

call_set_id = call_sets[0]['id']


# 2. Once we have the call set ID,
# lookup the variants that overlap the position we are interested in
request = service.variants().search(
    body={'callSetIds': [call_set_id],
          'referenceName': reference_name,
          'start': reference_position,
          'end': reference_position + 1},
    fields='variants(names,referenceBases,alternateBases,calls(genotype))')
variant = request.execute().get('variants', [])[0]

variant_name = variant['names'][0]
genotype = [variant['referenceBases'] if g == 0
            else variant['alternateBases'][g - 1]
            for g in variant['calls'][0]['genotype']]

print 'the called genotype is %s for %s' % (','.join(genotype), variant_name)
'''
if __name__ == '__main__':
    app.run(port=1028, debug=True, host='0.0.0.0')
