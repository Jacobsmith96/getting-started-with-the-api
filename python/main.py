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
dataset_id = '10473108253681171589'  # This is the 1000 Genomes dataset ID
sample = 'NA12872'
reference_name = '22'
reference_position = 51003835


# 1. First find the read group set ID for the sample
request = service.readgroupsets().search(
    body={'datasetIds': [dataset_id], 'name': sample},
    fields='readGroupSets(id)')
read_group_sets = request.execute().get('readGroupSets', [])
if len(read_group_sets) != 1:
  raise Exception('Searching for %s didn\'t return '
                  'the right number of read group sets' % sample)

read_group_set_id = read_group_sets[0]['id']

# 2. Once we have the read group set ID,
# lookup the reads at the position we are interested in
request = service.reads().search(
    body={'readGroupSetIds': [read_group_set_id],
          'referenceName': reference_name,
          'start': reference_position,
          'end': reference_position + 1},
    fields='alignments(alignment,alignedSequence)')
reads = request.execute().get('alignments', [])

# Note: This is simplistic - the cigar should be considered for real code
bases = [
    read['alignedSequence'][
        reference_position - int(read['alignment']['position']['position'])]
    for read in reads]

print '%s bases on %s at %d are' % (sample, reference_name, reference_position)
for base, count in Counter(bases).items():
  print '%s: %s' % (base, count)

#
# This example gets the variants for a sample at a specific position
#

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
