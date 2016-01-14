#!/usr/bin/env python
import sys, os
test_dir = '/tmp/'
src_dir = '../'
print("***" + test_dir)
sys.path.insert(0, os.path.abspath(os.path.join(test_dir, src_dir)))

from inscriptis import Parser
from bs4 import BeautifulSoup
import html2text

import lxml
import urllib
import time
import os
import time
from datetime import datetime

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

import subprocess
import threading
import operator

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

timestamp = str(datetime.now()).replace(" ", "_").replace(":", "-").split(".")[0]

def save_to_file(algorithm, url, data):
    with open(test_dir + '/comparison_results/' + timestamp + '/output_{}_{}.txt'.format(algorithm, url), 'w') as output_file:
        output_file.write(data)


def get_output_lynx(url):

    def kill_lynx(pid):
        os.kill(pid, signal.SIGKILL)
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
    soup = BeautifulSoup(input_data)

    for script in soup(["script", "style"]):
        script.extract()

    text = soup.get_text()
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    result = '\n'.join(chunk for chunk in chunks if chunk)

    return result


def get_clean_bs_html(input_data):
    soup = BeautifulSoup(input_data, "lxml")
    for script in soup(["script", "style"]):
        script.extract()

    return str(soup).strip('\t\r\n')


def get_output_html2cleartext(input_data):

    parser = Parser()
    parser.feed(input_data)
    result = parser.wiki.replace("* \n", "\n")

    while "\n\n\n" in result:
        result = result.replace("\n\n\n", "\n\n")

    return "".join(result)


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

    # These are a few predefined urls the script will
    sources = ["http://www.watson.de",
                     "http://www.watson.ch/Digital%20&%20Games/Android/134350872-Der-Monster-Akku-in-diesem-Smartphone-h%C3%A4lt-bis-15-Tage",
                     "http://www.heise.de",
                     "http://www.heise.de/newsticker/meldung/Fairphone-2-im-Test-Das-erste-modulare-Smartphone-3043417.html",
                     "http://www.nzz.de",
                     "http://www.nzz.ch/mobilitaet/auto-mobil/bekenntnis-zum-stromauto-ld.3630",
                     "https://de.wikipedia.org/wiki/Wikipedia:Hauptseite",
                     "https://de.wikipedia.org/wiki/Python_(Programmiersprache)",
                     "https://de.wikipedia.org/wiki/Chur",
                     "http://jr-central.co.jp",
                     "http://www.aljazeera.net/portal",
                     "http://www.aljazeera.net/news/humanrights/2015/12/14/%D8%A3%D9%88%D8%A8%D8%A7%D9%85%D8%A7-%D9%8A%D8%AC%D8%AF%D8%AF-%D8%A7%D9%84%D8%AA%D8%B2%D8%A7%D9%85%D9%87-%D8%A8%D8%A5%D8%BA%D9%84%D8%A7%D9%82-%D8%BA%D9%88%D8%A7%D9%86%D8%AA%D8%A7%D9%86%D8%A7%D9%85%D9%88",
                     "http://www.htwchur.ch"]

    if not os.path.exists(test_dir + '/comparison_results'):
        os.makedirs(test_dir + '/comparison_results')

    if not os.path.exists(test_dir + '/comparison_results/' + timestamp):
        os.makedirs(test_dir + '/comparison_results/'  + timestamp)

    with open(test_dir + '/comparison_results/' + timestamp + '/speed_comparisons.txt', 'w') as output_file:
            output_file.write("")

    for source in sources:

        html = urllib.request.urlopen(source)
        html_source = get_clean_bs_html(html.read())
        source_name = source

        trash = (("http://", ""),
                      ("https://", ""),
                      ("/", "-"),
                      (":", "-"),
                      ("%", ""))

        for key, value in trash:
            source_name = source_name.replace(key, value)
        source_name = source_name[0:100]

        with open(test_dir + '/comparison_results/' + timestamp + '/speed_comparisons.txt', 'a') as output_file:
            output_file.write("\nURL: {}\n".format(source_name))
        print("\nURL: {}".format(source_name))

        times = {}

        if lynx_available:
            algorithm = "lynx"
            start_time = time.time()
            data = get_output_lynx(source)
            stop_time = time.time()
            times[algorithm] = stop_time - start_time
            save_to_file(algorithm, source_name, data)


        if justext_available:
            algorithm = "justext"
            start_time = time.time()
            data = get_output_justext(html_source)
            stop_time = time.time()
            times[algorithm] = stop_time - start_time
            save_to_file(algorithm, source_name, data)

        if html2text_available:
            algorithm = "html2text"
            start_time = time.time()
            data = get_output_html2text(html_source)
            stop_time = time.time()
            times[algorithm] = stop_time - start_time
            save_to_file(algorithm, source_name, data)


        algorithm = "beautifulsoup"
        start_time = time.time()
        data = get_output_beautifulsoup(html.read())
        stop_time = time.time()
        times[algorithm] = stop_time - start_time
        save_to_file(algorithm, source_name, data)


        algorithm = "spiffwiki"
        start_time = time.time()
        data = get_output_html2cleartext(html_source)
        stop_time = time.time()
        times[algorithm] = stop_time - start_time
        save_to_file(algorithm, source_name, data)

        speed_table = get_speed_table(times)
        print(speed_table)

        with open(test_dir + '/comparison_results/' + timestamp + '/speed_comparisons.txt', 'a') as output_file:
            output_file.write(speed_table + "\n")
    with open(test_dir + '/comparison_results/' + timestamp + '/speed_comparisons.txt', 'a') as output_file:
        output_file.write("\n")

if __name__ == "__main__":
    pipeline()



