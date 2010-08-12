
import sys
import os
import csv
import logging

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import tornado.options

def run(input_filename, output_file_format):
    input_file = open(input_filename, 'rb')
    reader = csv.reader(input_file)
    for row in reader:
        if not row or len(row) < 43:
            continue
        for block in _block(row):
            logging.info(block)
    
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
    tornado.options.define('output_format', type=str, help="format for output turnstile_YYMMDD.csv file", default="turnstile_%Y%m%d.csv")
    tornado.options.parse_command_line()

    input_file = tornado.options.options.input_file
    assert os.path.exists(input_file)

    run(input_file, tornado.options.options.output_format)