"""
This takes a mta .txt data dump, and normalizes it to a single set of columns so it's a file that can be combined/sorted with other data sets
"""

import sys
import os
import csv
import logging

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import tornado.options

def run(input_filename, output_filename):
    logging.info('reading %s' % input_filename)
    logging.info('outputing to %s' % output_filename)
    input_file = open(input_filename, 'rb')
    output_file = open(output_filename, 'ab')
    writer = csv.writer(output_file)
    reader = csv.reader(input_file)
    
    rows = 0
    for row in reader:
        if not row or len(row) < 43:
            continue
        for block in _block(row):
            rows += 1
            writer.writerow(block)
    logging.info('output %d records' % rows)
    input_file.close()
    output_file.close()
    
def _block(data):
    #C/A,UNIT,SCP,DATE1,TIME1,DESC1,ENTRIES1,EXITS1,DATE2,TIME2,DESC2,ENTRIES2,EXITS2,DATE3,TIME3,DESC3,ENTRIES3,EXITS3,DATE4,TIME4,DESC4,ENTRIES4,EXITS4,DATE5,TIME5,DESC5,ENTRIES5,EXITS5,DATE6,TIME6,DESC6,ENTRIES6,EXITS6,DATE7,TIME7,DESC7,ENTRIES7,EXITS7,DATE8,TIME8,DESC8,ENTRIES8,EXITS8
    ca = data.pop(0)
    unit = data.pop(0)
    scp = data.pop(0)
    data[-1] = data[-1].rstrip()
    while len(data) >=5:
        block, data = data[:5], data[5:] # DATE1,TIME1,DESC1,ENTRIES1,EXITS1
        yield [ca, unit, scp] + block



if __name__ == "__main__":
    tornado.options.define('input_file', type=str, help="input turnstile_YYMMDD.txt file")
    tornado.options.define('output_file', type=str, help="output to global data file", default="../data/complete.csv")
    tornado.options.parse_command_line()

    input_file = tornado.options.options.input_file
    assert os.path.exists(input_file)

    run(input_file, tornado.options.options.output_file)