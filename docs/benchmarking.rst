====================================
Testing, benchmarking and evaluation
====================================

Unit tests
----------
Test cases concerning the html to text conversion are located in the `tests/html` directory and consist of two files:

 1. `test-name.html` and
 2. `test-name.txt`

the latter one containing the reference text output for the given html file.


Text conversion output comparison and speed benchmarking
--------------------------------------------------------
The inscriptis project contains a benchmarking script that can compare different HTML to text conversion approaches.
The script will run the different approaches on a list of URLs, `url_list.txt`, and save the text output into a time stamped folder in `benchmarking/benchmarking_results` for manual comparison.
Additionally the processing speed of every approach per URL is measured and saved in a text file called `speed_comparisons.txt` in the respective time stamped folder.

To run the benchmarking script execute `run_benchmarking.py` from within the folder `benchmarking`.
In `def pipeline()` set the which HTML -> Text algorithms to be executed by modifying::

   run_lynx = True
   run_justext = True
   run_html2text = True
   run_beautifulsoup = True
   run_inscriptis = True

In `url_list.txt` the URLs to be parsed can be specified by adding them to the file, one per line with no additional formatting. URLs need to be complete (including http:// or https://)
e.g.::

   http://www.informationscience.ch
   https://en.wikipedia.org/wiki/Information_science
   ...

