---
title: 'Inscriptis - A Python-based HTML to text conversion library optimized for knowledge extraction from the Web'
tags:
  - Python
  - Web mining
  - Knowledge Extraction
  - text conversion
  - gold standard creation
  - annotated text output
authors:
  - name: Albert Weichselbraun^[corresponding author]
    orcid: 0000-0001-6399-045X
    affiliation: 1
affiliations:
 - name: University of Applied Sciences of the Grisons, Chur, Switzerland
   index: 1
date: 25 June 2021
bibliography: paper.bib
--- 

# Summary

``Inscriptis`` provides a library, command line client and Web service for converting HTML content to plain text. In contrast to existing software packages such as [HTML2text](https://github.com/Alir3z4/html2text/), [Justext](https://github.com/miso-belica/jusText/) and [Lynx](https://lynx.invisible-island.net/), it has been tailored towards text processing pipelines by 

1. providing a layout-aware rendering of textual output that in many cases closely resembles the rendering obtained from standard Web browsers. ``Inscriptis`` excels in terms of conversion quality, since it is able to correctly interpret complex HTML constructs such as nested tables and also supports a subset of HTML (e.g., `align`, `valign`) and CSS (e.g., `display`, `white-space`, `margin-top`, `vertical-algin`, etc.) attributes that determine the text alignment.
 2. supporting annotation rules, i.e., user-provided mappings that allow for annotating the extracted text based on structural and semantic information encoded in HTML tags and attributes used for controlling structure and layout in the original HTML document. 

These unique features ensure that downstream Knowledge Extraction components can operate on accurate text representations of the original input without drawing upon heavyweight solutions such as [Selenium](https://www.selenium.dev/) which require interaction with a full-fledged Web browser. In addition, its optional annotation support enables downstream components to use information on the structure of the original HTML document.


# Statement of need

Research in an ever growing number of scientific disciplines relies upon Web content. @li_effect_2014, for instance, studied the impact of company-specific News coverage on stock prices, in medicine and for pharmacovigilance social media listening plays an important role in gathering insights into patient needs and the monitoring of adverse drug effects [@convertino_usefulness_2018], and communication sciences draw upon media coverage to obtain information on the perception and framing of issues as well as the rise and fall of topics within News media [@scharl2017; @weichselbraun_adapting_2021].

Computer science focuses on analyzing content by applying knowledge extraction techniques such as entity recognition [@fu_spanner_2021] to automatically identify entities (e.g., persons, organizations, locations, products, etc.) within text documents, entity linking [@ding_jel_2021] to link these entities to knowledge bases (e.g., Wikidata and DBPedia), and sentiment analysis to automatically assess sentiment polarity (i.e., positive versus negative coverage) and emotions expressed towards these entities [@wang_review_2020].

Most of these methods operate on textual content and require the conversion of the HTML content to plain text. Some social media platforms (e.g., Twitter and Youbube) provide APIs that allow researchers to easily access the textual content, but the majority of Web content still is only accessible in the HTML format and requires translation prior to its use in Knowledge Extraction pipelines.

Many standard HTML to text conversion approaches are not layout aware and, therefore, often yield text that fails to accurately represent the spatial arrangement of elements as illustrated in the figure below.

![Text representation of a table from DBpedia computed by ``Inscriptis`` (left) and lynx (right) with the options `-nolist -width=500`. Lynx fails to correctly interpret the cascaded table and, therefore, does not correctly align the temperature values.](images/inscriptis-vs-lynx.png)

``Inscriptis`` is not only able to correctly render such pages but also offers the option to preserve parts of the original HTML document's semantics (e.g., information on headings, emphasised text, tables, etc.). \autoref{fig:annotations} provides an example of annotations extracted from a Wikipedia page. These annotations might be useful to

- aid downstream Knowledge Extraction components with additional information that may be leveraged to improve their respective performance. Text summarization techniques, for instance, can put a stronger emphasis on paragraphs that contain bold and italic text, and sentiment analysis may consider this information in addition to textual clues such as uppercase text.
- assist manual document annotation processes (e.g., for qualitative analysis or gold standard creation). ``Inscripti``s supports multiple export formats such as XML, annotated HTML and the JSONL format that is used by the open source annotation tool [doccano](https://github.com/doccano/doccano) (please note that doccano currently is not able to import JSONL files which contain overlapping annotations.). Support for further annotation formats can be easily added by implementing custom annotation processors.
- enable the use of ``Inscriptis``  for tasks such as content extraction (i.e., extract task-specific relevant content from a Web page) which rely on information on the HTML document's structure.

![Snippet of the annotations extracted from the DBpedia entry for Chur which has been exported using the HTML annotation processor.\label{fig:annotations}](images/annotations.png)

In conclusion, ``Inscriptis`` plays an important role in providing Knowledge Extraction components with high quality conversions of HTML documents. ``Inscriptis`` has been constantly improved in more than five years of development, has proven its capabilities in national and European research projects and has been integrated into commercial products such as the [webLyzard Web Intelligence and Visual Analytics Platform](https://www.weblyzard.com/visual-analytics-dashboard/).



# Mentions

``Inscriptis`` has been actively used within the following research projects

- [CareerCoach](https://www.fhgr.ch/CareerCoach): Automatic Knowledge Extraction and Recommender Systems for Personalized Re- and Upskilling suggestions funded by Innosuisse.
- [EPOCH project](https://www.epoch-project.eu) funded by the Austrian Federal Ministry for Climate Action, Environment, Energy, Mobility and Technology (BMK) via the ICT of the Future Program.
- [MedMon](https://www.fhgr.ch/medmon): Monitoring of Internet Resources for Pharamceutical Research and Development funded by Innosuisse.
- [ReTV project](https://www.retv-project.eu) funded by the European Union’s Horizon 2020 Research and Innovation Programme.


# Acknowledgements

Work on ``Inscriptis`` has been conducted within the MedMon and CareerCoach projects funded by Innosuisse, and has been supported by the webLyzard technology gmbh.


# References

