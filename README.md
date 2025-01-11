This program can be used to covert a transcript coordinate into a genomic coordinate based on the mapping as specified
using a CIGAR string.

The program makes 2 key assumptions that:
    1. The mapping file that specifies the transcripts name, chromosome name, mapping coordinate and the CIGAR string
        will contain unique values of the transcript names; i.e., transcript names are not repeated across the rows.
    1. Only "M", "D" and "I" are the valid mapping types in a cigar string. Other non-cannonical mapping types such as
        "S", "N", "H", "P", etc are not accounted for. The program will error out is anything other than M", "D" and
        "I" is encountered.

The program is written using Python 3.8.10, and can be invoked as follows:
    python tx_to_genomic_coordinates.py -t test/truth_mapping.tsv -q test/queries_fail_tx1.tsv
  
An output file ending with "_genome_coordinates.txt" will be output to the same directory as the input query file.

Test files and outputs are included in the /test directory.

Accuracy of the program and the functions within can also be tested using the "pytest" module. I have written unit
tests for the underlying function in tests.py. Pytest can be invoked using :
    pytest ./tests.py
