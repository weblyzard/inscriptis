====================================
Testing, benchmarking and evaluation
====================================

Unit tests
==========
In addition to the standard unit tests that are located in the project's `test` directory Inscriptis also contains 
test cases that solely focus on the html to text conversion and are located in the `tests/html` directory. 
These tests consist of two files:

 1. `test-name.html` and
 2. `test-name.txt`

The `.txt` file contains the reference text output for the given html file.

Since Inscripits 2.0 there may also be a third file named `test-name.json` in the `tests/html` directory which contains a JSON dictioanry with keys

 1. `annotation-rules` containing the annotation rules for extracting metadata from the corresponding html file, and
 2. `result` which stores the surface forms of the extracted metadata.


Example::

	{"annotation_rules": {
	    "h1": ["heading"],
	    "b": ["emphasis"]
	 },
	 "result": [
		["heading", "The first"],
		["heading", "The second"],
		["heading", "Subheading"]
	 ]
	}


Text conversion output comparison and benchmarking
==================================================
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

