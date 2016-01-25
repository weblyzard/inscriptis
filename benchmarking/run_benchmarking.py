#!/usr/bin/env python3
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

TRIES = 5

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
timestamp = str(datetime.now()).replace(" ", "_").replace(":", "-").split(".")[0]
benchmarking_results_dir = os.path.join(benchmarking_root, 'benchmarking_results', timestamp)
cache_dir = os.path.join(benchmarking_root, 'html_cache')

src_dir = os.path.join(benchmarking_root, '../src')
sys.path.insert(0, os.path.abspath(src_dir))
import inscriptis



def save_to_file(algorithm, url, data):
    result_file = os.path.join(benchmarking_results_dir, '{}_{}.txt'.format(algorithm, url))
    with open(result_file, 'w') as output_file:
        output_file.write(data)

def get_output_lynx(html):

    def kill_lynx(pid):
        os.kill(pid, os.signal.SIGKILL)
        os.waitpid(-1, os.WNOHANG)
        print("lynx killed")

    web_data = ""

    lynx_args = '-stdin -width=20000 -force_html -nocolor -dump -nolist -nobold -display_charset=utf8'
    cmd = ["/usr/bin/lynx", ] + lynx_args.split(" ")
    lynx = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    lynx.stdin.write(html.encode("utf8"))
    lynx.stdin.close()
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

def clean_source_name(src):
    trash = (("http://", ""),
             ("https://", ""),
             ("/", "-"),
             (":", "-"),
             ("%", ""))

    for key, value in trash:
        src = src.replace(key, value)
    return src[0:100]


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

    if not os.path.exists(benchmarking_results_dir):
        os.makedirs(benchmarking_results_dir)

    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)

    with open(os.path.join(benchmarking_results_dir, 'speed_comparisons.txt'), 'w') as output_file:
            output_file.write("")

    for source in sources:

        source_name = clean_source_name(source)
        source_cache_path= os.path.join(cache_dir, source_name)
        if os.path.exists(source_cache_path):
            html = open(source_cache_path).read()
        else:
            try:
                html = urllib.request.urlopen(source).read().decode("utf-8")
            except UnicodeDecodeError:
                html = urllib.request.urlopen(source).read().decode("latin1")
            open(source_cache_path, 'w').write(html)

        with open(os.path.join(benchmarking_results_dir, 'speed_comparisons.txt'), 'a') as output_file:
            output_file.write("\nURL: {}\n".format(source_name))
        print("\nURL: {}".format(source_name))

        times = {}

        if run_lynx and lynx_available:
            algorithm = "lynx"
            start_time = time.time()
            for n in range(TRIES):
                data = get_output_lynx(html)
            stop_time = time.time()
            times[algorithm] = stop_time - start_time
            save_to_file(algorithm, source_name, data)

        if run_justext and justext_available:
            algorithm = "justext"
            start_time = time.time()
            for n in range(TRIES):
                data = get_output_justext(html)
            stop_time = time.time()
            times[algorithm] = stop_time - start_time
            save_to_file(algorithm, source_name, data)

        if run_html2text and html2text_available:
            algorithm = "html2text"
            start_time = time.time()
            for n in range(TRIES):
                data = get_output_html2text(html)
            stop_time = time.time()
            times[algorithm] = stop_time - start_time
            save_to_file(algorithm, source_name, data)

        if run_beautifulsoup:
            algorithm = "beautifulsoup"
            start_time = time.time()
            for n in range(TRIES):
                data = get_output_beautifulsoup(html)
            stop_time = time.time()
            times[algorithm] = stop_time - start_time
            save_to_file(algorithm, source_name, data)

        if run_inscriptis:
            algorithm = "inscriptis"
            start_time = time.time()
            for n in range(TRIES):
                data = inscriptis.get_text(html)
            stop_time = time.time()
            times[algorithm] = stop_time - start_time
            save_to_file(algorithm, source_name, data)

        speed_table = get_speed_table(times)
        print(speed_table)

        with open(os.path.join(benchmarking_results_dir, 'speed_comparisons.txt'), 'a') as output_file:
            output_file.write(speed_table + "\n")
    with open(os.path.join(benchmarking_results_dir, 'speed_comparisons.txt'), 'a') as output_file:
        output_file.write("\n")

if __name__ == "__main__":
    pipeline()
