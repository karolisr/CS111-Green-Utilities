# -*- coding: utf-8 -*-
"""Read / Write sequence files."""

def write_genbank_records(gb_records, file):  # noqa
    if type(gb_records) in (list, tuple):
        gb_records_string = '\n\n'.join(gb_records)
    else:
        gb_records_string = gb_records
    with open(file, 'w') as f:
        f.write(gb_records_string)
