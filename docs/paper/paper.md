---
title: 'Inscriptis - A Python-based HTML to text conversion library optimized for knowledge extraction from the Web'
tags:
  - Python
  - web mining
  - knowledge extraction
  - text conversion
  - gold standard creation
  - annotated text output
authors:
  - name: Albert Weichselbraun
    orcid: 0000-0001-6399-045X
    affiliation: 1
affiliations:
 - name:  Swiss Institute for Information Science, University of Applied Sciences of the Grisons, Pulvermühlestrasse 57, Chur, Switzerland
   index: 1
date: 25 June 2021
bibliography: paper.bib
---  
 
# Summary
 
``Inscriptis`` provides a library, command line client and Web service for converting HTML to plain text.
 
Its development has been triggered by the need to obtain accurate text representations for knowledge extraction tasks that preserve the spatial alignment of text without drawing upon heavyweight, browser-based solutions such as Selenium [@selenium].
In contrast to existing software packages such as HTML2text [@html2text], jusText [@justext] and Lynx [@lynx], ``Inscriptis``
 
1. provides a layout-aware conversion of HTML that more closely resembles the rendering obtained from standard Web browsers and, therefore, better preserves the spatial arrangement of text elements. ``Inscriptis`` excels in terms of conversion quality, since it correctly converts complex HTML constructs such as nested tables and also interprets a subset of HTML (e.g., `align`, `valign`) and CSS (e.g., `display`, `white-space`, `margin-top`, `vertical-align`, etc.) attributes that determine the text alignment.
2. supports annotation rules, i.e., user-provided mappings that allow for annotating the extracted text based on structural and semantic information encoded in HTML tags and attributes used for controlling structure and layout in the original HTML document.
 
These unique features ensure that downstream knowledge extraction components can operate on accurate text representations, and may even use information on the semantics and structure of the original HTML document, if annotation support has been enabled.
 
 
# Statement of need
 
Research in a growing number of scientific disciplines relies upon Web content. @li_effect_2014, for instance, studied the impact of company-specific News coverage on stock prices, in medicine and pharmacovigilance social media listening plays an important role in gathering insights into patient needs and the monitoring of adverse drug effects [@convertino_usefulness_2018], and communication sciences analyze media coverage to obtain information on the perception and framing of issues as well as on the rise and fall of topics within News and social media [@scharl_semantic_2017; @weichselbraun_adapting_2021].
 
Computer science focuses on analyzing content by applying knowledge extraction techniques such as entity recognition [@fu_spanner_2021] to automatically identify entities (e.g., persons, organizations, locations, products, etc.) within text documents, entity linking [@ding_jel_2021] to link these entities to knowledge bases such as Wikidata and DBPedia, and sentiment analysis to automatically assess sentiment polarity (i.e., positive versus negative coverage) and emotions expressed towards these entities [@wang_review_2020].
 
Most knowledge extraction methods operate on text and, therefore, require an accurate conversion of HTML content which also preserves the spatial alignment between text elements. This is particularly true for methods drawing upon algorithms which directly or indirectly leverage information on the proximity between terms, such as word embeddings [@mikolov_distributed_2013; @pennington_glove:_2014], language models [@reis_transformers_2021], sentiment analysis which often also considers the distance between target and sentiment terms, and automatic keyword and phrase extraction techniques.
 
Despite this need from within the research community, many standard HTML to text conversion techniques are not layout aware, yielding text representations that fail to preserve the text's spatial properties, as illustrated below:
 
![Text representation of a table from Wikipedia computed by ``Inscriptis`` (left) and Lynx (right). Lynx fails to correctly interpret the table and, therefore, does not properly align the temperature values.](images/inscriptis-vs-lynx.png)

Consequently, even popular resources extensively used in literature suffer from such shortcomings. The text representations provided with the Common Crawl corpus^[https://commoncrawl.org/], for instance, have been generated with a custom utility [@ia-commons] which at the time of writing did not consider any layout information. Datasets such as CCAligned [@el-kishky_ccaligned_2020], multilingual C4 which has been used for training the mT5 language model [@xue_mt5_2021], and OSCAR [@suarez_asynchronous_2019] are based on subsets of the Common Crawl corpus [@caswell_quality_2021].

Even worse, some tutorials suggest the use of software libraries such as Beautiful Soup [@beautifulsoup], lxml [@lxml] and Cheerio [@cheerio] for converting HTML. Since these libraries have been designed with a different use case in mind, they are only well-suited for scraping textual content. Once they encounter HTML constructs such as lists and tables, these libraries are likely to return artifacts (e.g., concatenated words), since they do not interpret HTML semantics. The creators of the Cheerio library even warn their users, by explicitly stating that it is not well-suited for emulating Web browsers.

Specialized conversion tools such as HTML2Text perform considerably better but often fail for more complex Web pages. Researchers sometimes even draw upon text-based Web browsers such as Lynx to obtain more accurate representations of HTML pages. These tools are complemented by content extraction software such as jusText [@justext], dragnet [@peters_content_2013], TextSweeper [@lang_textsweeper_2012] and boilerpy3 [@boilerpy3] which do not consider the page layout but rather aim at extracting the relevant content only, and approaches that are optimized for certain kinds of Web pages like Harvest [@weichselbraun_harvest_2020] for Web forums.

``Inscriptis``, in contrast, not only correctly renders more complex websites but also offers the option to preserve parts of the original HTML document's semantics (e.g., information on headings, emphasized text, tables, etc.) by complementing the extracted text with annotations obtained from the document. \autoref{fig:annotations} provides an example of annotations extracted from a Wikipedia page. These annotations can be useful for
 
- providing downstream knowledge extraction components with additional information that may be leveraged to improve their respective performance. Text summarization techniques, for instance, can put a stronger emphasis on paragraphs that contain bold and italic text, and sentiment analysis may consider this information in addition to textual clues such as uppercase text.
- assisting manual document annotation processes (e.g., for qualitative analysis or gold standard creation). ``Inscriptis`` supports multiple export formats such as XML, annotated HTML and the JSONL format that is used by the open source annotation tool doccano^[Please note that doccano currently does not support overlapping annotations and, therefore, cannot import files containing overlapping annotations.] [@doccano]. Support for further annotation formats can be easily added by implementing custom annotation post-processors.
- enabling the use of ``Inscriptis``  for tasks such as content extraction (i.e., extract task-specific relevant content from a Web page) which rely on information on the HTML document's structure.
 
![Annotations extracted from the Wikipedia entry for Chur that have been exported to HTML using the ``--postprocessor html`` command line option.\label{fig:annotations}](images/annotations.png)
 
In conclusion, ``Inscriptis`` provides knowledge extraction components with high quality text representations of HTML documents.
Since its first public release in March 2016, ``Inscriptis`` has been downloaded over 135,000 times from the Python Package Index (PyPI)^[Source: https://pepy.tech/project/inscriptis], has proven its capabilities in national and European research projects, and has been integrated into commercial products such as the [webLyzard Web Intelligence and Visual Analytics Platform](https://www.weblyzard.com/visual-analytics-dashboard/).
 
 
 
# Mentions
 
The following research projects use ``Inscriptis`` within their knowledge extraction pipelines:
 
- [CareerCoach](https://www.fhgr.ch/CareerCoach): "Automatic Knowledge Extraction and Recommender Systems for Personalized Re- and Upskilling suggestions" funded by Innosuisse.
- [Job Cockpit](https://www.fhgr.ch/Job-Cockpit): "Web analytics, data enrichment and predictive analysis for improved recruitment and career management processes" funded by Innosuisse
- [EPOCH project](https://www.epoch-project.eu) funded by the Austrian Federal Ministry for Climate Action, Environment, Energy, Mobility and Technology (BMK) via the ICT of the Future Program.
- [MedMon](https://www.fhgr.ch/medmon): "Monitoring of Internet Resources for Pharmaceutical Research and Development" funded by Innosuisse.
- [ReTV project](https://www.retv-project.eu) funded by the European Union’s Horizon 2020 Research and Innovation Programme.
 
 
# Acknowledgements
 
Work on ``Inscriptis`` has been conducted within the MedMon, Job Cockpit and CareerCoach projects funded by Innosuisse.
 
 
# References

