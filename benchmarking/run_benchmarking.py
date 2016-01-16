#!/usr/bin/env python
# coding:utf-8
"""
Runs a benchmarking suite to compare speed
and output of different implementations.
"""

__author__ = "Fabian Odoni, Albert Weichselbraun"
__copyright__ = "Copyright 2015, HTW Chur"
__license__ = "GPL"
__version__ = "0.0.1"
__maintainer__ = "Fabian Odoni"
__email__ = "fabian.odoni@htwchur.ch"
__status__ = "Prototype"

from bs4 import BeautifulSoup
from datetime import datetime
import operator
import os
import subprocess
import sys
import threading
import time
import urllib

try:
    import justext
    justext_available = True
except:
    justext_available = False
    print('justext not available. Please install in order to compare with justext.')

try:
    import html2text
    html2text_available = True
except:
    html2text_available = False
    print('html2text not available. Please install in order to compare with html2text.')

try:
    subprocess.call(["lynx", "-dump \"www.google.com\""], stdout=subprocess.PIPE)
    # subprocess.Popen(["lynx", "-dump \"www.google.com\""], shell=True, stdout=subprocess.PIPE)
    lynx_available = True
except OSError as e:
    if e.errno == os.errno.ENOENT:
        print('lynx can not be called. Please check in order to compare with lynx.')
        lynx_available = False
    else:
        print('lynx can not be called. Please check in order to compare with lynx.')
        lynx_available = False
        raise

benchmarking_root = os.path.dirname(os.path.abspath(__file__))
benchmarking_results_dir = '/benchmarking_results/'
src_dir = os.path.join(benchmarking_root, '../src')
sys.path.insert(0, os.path.abspath(src_dir))
import inscriptis

timestamp = str(datetime.now()).replace(" ", "_").replace(":", "-").split(".")[0]


def save_to_file(algorithm, url, data):
    with open(benchmarking_root + benchmarking_results_dir + timestamp + '/output_{}_{}.txt'.format(algorithm, url), 'w') as output_file:
        output_file.write(data)


def get_output_lynx(url):

    def kill_lynx(pid):
        os.kill(pid, os.signal.SIGKILL)
        os.waitpid(-1, os.WNOHANG)
        print("lynx killed")

    web_data = ""

    lynx_args = '-width=20000 -force_html -nocolor -dump -nolist -nobold -display_charset=utf8'
    cmd = "/usr/bin/lynx {} \"{}\"".format(lynx_args, url)
    lynx = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    t = threading.Timer(200.0, kill_lynx, args=[lynx.pid])
    t.start()

    web_data = lynx.stdout.read()
    t.cancel()

    web_data = web_data.decode("utf-8", 'replace')
    return web_data


def get_output_justext(input_data):
    result = []
    paragraphs = justext.justext(input_data, stoplist='English')
    for paragraph in paragraphs:
        result.append(paragraph.text)

    return "\n".join(result)


def get_output_html2text(input_data):
    h = html2text.HTML2Text()
    h.ignore_links = True
    result = h.handle(str(input_data))

    return "".join(result)


def get_output_beautifulsoup(input_data):
    soup = BeautifulSoup(input_data, "lxml")

    for script in soup(["script", "style"]):
        script.extract()

    text = soup.get_text()
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    result = '\n'.join(chunk for chunk in chunks if chunk)

    return result


def get_speed_table(times):
    fastest = 999999
    for key, value in times.items():
        if value < fastest:
            fastest = value

    longest_key = 0
    longest_value = 0
    for key, value in times.items():
        if len(key) > longest_key:
            longest_key = len(key)
        if len(str(value)) > longest_value:
            longest_value = len(str(value))

    sorted_times = sorted(times.items(), key=operator.itemgetter(1))

    result = ''
    for key, value in sorted_times:
        difference = value - fastest
        if difference > 0:
            difference = '+{}'.format(difference)
        elif difference < 0:
            difference = "-{}".format(difference)
        elif difference == 0:
            difference = "--> fastest".format(difference)

        output = "{}{}: {}{} {}".format(key, ' ' * (longest_key - len(key)), value, ' ' * (longest_value - len(str(value))), difference)
        result += output + '\n'

    return result


def pipeline():
    run_lynx = True
    run_justext = True
    run_html2text = True
    run_beautifulsoup = True
    run_inscriptis = True

    # These are a few predefined urls the script will
    sources = []
    with open(os.path.join(benchmarking_root, 'url_list.txt')) as url_list:
        for line in url_list:
            sources.append(line.strip())

    if not os.path.exists(benchmarking_root + benchmarking_results_dir[:-1]):
        os.makedirs(benchmarking_root + benchmarking_results_dir[:-1])

    if not os.path.exists(benchmarking_root + benchmarking_results_dir + timestamp):
        os.makedirs(benchmarking_root + benchmarking_results_dir + timestamp)

    with open(benchmarking_root + benchmarking_results_dir + timestamp + '/speed_comparisons.txt', 'w') as output_file:
            output_file.write("")

    for source in sources:

        html = urllib.request.urlopen(source)
        html = inscriptis.clean_html(html.read())

        source_name = source

        trash = (("http://", ""),
                 ("https://", ""),
                 ("/", "-"),
                 (":", "-"),
                 ("%", ""))

        for key, value in trash:
            source_name = source_name.replace(key, value)
        source_name = source_name[0:100]

        with open(benchmarking_root + benchmarking_results_dir + timestamp + '/speed_comparisons.txt', 'a') as output_file:
            output_file.write("\nURL: {}\n".format(source_name))
        print("\nURL: {}".format(source_name))

        times = {}

        if run_lynx and lynx_available:
            algorithm = "lynx"
            start_time = time.time()
            data = get_output_lynx(source)
            stop_time = time.time()
            times[algorithm] = stop_time - start_time
            save_to_file(algorithm, source_name, data)

        if run_justext and justext_available:
            algorithm = "justext"
            start_time = time.time()
            data = get_output_justext(html)
            stop_time = time.time()
            times[algorithm] = stop_time - start_time
            save_to_file(algorithm, source_name, data)

        if run_html2text and html2text_available:
            algorithm = "html2text"
            start_time = time.time()
            data = get_output_html2text(html)
            stop_time = time.time()
            times[algorithm] = stop_time - start_time
            save_to_file(algorithm, source_name, data)

        if run_beautifulsoup:
            algorithm = "beautifulsoup"
            start_time = time.time()
            data = get_output_beautifulsoup(html)
            stop_time = time.time()
            times[algorithm] = stop_time - start_time
            save_to_file(algorithm, source_name, data)

        if run_inscriptis:
            algorithm = "inscriptis"
            start_time = time.time()
            data = inscriptis.get_text_from_html(html)
            stop_time = time.time()
            times[algorithm] = stop_time - start_time
            save_to_file(algorithm, source_name, data)

        speed_table = get_speed_table(times)
        print(speed_table)

        with open(benchmarking_root + benchmarking_results_dir + timestamp + '/speed_comparisons.txt', 'a') as output_file:
            output_file.write(speed_table + "\n")
    with open(benchmarking_root + benchmarking_results_dir + timestamp + '/speed_comparisons.txt', 'a') as output_file:
        output_file.write("\n")

if __name__ == "__main__":
    pipeline()
