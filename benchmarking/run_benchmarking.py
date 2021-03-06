#!/usr/bin/env python3
# coding:utf-8
'''
Runs a benchmarking suite to compare speed
and output of different implementations.
'''

from datetime import datetime
import operator
import os
import signal
import subprocess
import sys
import threading
import urllib.request

from time import time

#
# Import inscriptis (using the version in the project directory rather than
# any installed module versions).
#
LYNX_BIN = '/usr/bin/lynx'
BENCHMARKING_ROOT = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(BENCHMARKING_ROOT, '../src')
sys.path.insert(0, os.path.abspath(SRC_DIR))

try:
    import inscriptis
except ImportError:
    print('Inscriptis is not available. Please install it in order to '
          'compare with inscriptis.')

#
# Import third-party HTML 2 text converters.
#
try:
    from bs4 import BeautifulSoup
except ImportError:
    print('BeautifulSoup is not available. Please install it in order to '
          'compare with BeautifulSoup.')
try:
    import html2text
except ImportError:
    print('html2text is not available. Please install it in order to '
          'compare with html2text.')
try:
    import justext
except ImportError:
    print('justext is not available. Please install it in order to compare '
          'with justext.')


TRIES = 7
OUTFILE = 'speed_comparisons.txt'


class AbstractHtmlConverter():
    '''
    An abstract HTML convert class.
    '''

    def get_text(self, html):
        '''
        Returns:
            a text representation of the given HTML snippet.
        '''
        raise NotImplementedError

    def benchmark(self, html):
        '''
        Benchmarks the classes HTML to text converter.

        Returns:
            A tuple of the required time and the obtained text representation.
        '''
        start_time = time()
        for _ in range(TRIES):
            text = self.get_text(html)
        return time() - start_time, text


class BeautifulSoupHtmlConverter(AbstractHtmlConverter):
    '''
    Converts HTML to text using BeautifulSoup.
    '''
    name = 'BeautifulSoup'

    def __init__(self):
        self.available = 'bs4' in sys.modules

    def get_text(self, html):
        soup = BeautifulSoup(html, 'lxml')

        for script in soup(['script', 'style']):
            script.extract()

        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines
                  for phrase in line.split('  '))
        result = '\n'.join(chunk for chunk in chunks if chunk)
        return result


class JustextHtmlConverter(AbstractHtmlConverter):
    '''
    Converts HTML to text using Justtext.
    '''
    name = 'Justtext'

    def __init__(self):
        self.available = 'justext' in sys.modules

    def get_text(self, html):
        paragraphs = justext.justext(html, stoplist='English')
        result = [paragraph.text for paragraph in paragraphs]
        return '\n'.join(result)


class Html2TextConverter(AbstractHtmlConverter):
    '''
    Converts HTML to text using Html2Text.
    '''
    name = 'Html2Text'

    def __init__(self):
        self.available = 'html2text' in sys.modules

    def get_text(self, html):
        converter = html2text.HTML2Text()
        converter.ignore_links = True
        result = converter.handle(str(html))

        return ''.join(result)


class LynxHtmlConverter(AbstractHtmlConverter):
    '''
    Converts HTML to text using lynx.
    '''
    name = 'lynx'

    def __init__(self):
        try:
            subprocess.call([LYNX_BIN, '-dump \'www.google.com\''],
                            stdout=subprocess.PIPE)
            self.available = True
        except OSError:
            print('lynx can not be called. Please check in order to compare '
                  'with lynx.')
            self.available = False

    def get_text(self, html):

        def kill_lynx(pid):
            os.kill(pid, signal.SIGKILL)
            os.waitpid(-1, os.WNOHANG)
            print('lynx killed')

        text = ''
        lynx_args = '-stdin -width=20000 -force_html -nocolor -dump -nolist ' \
                    '-nobold -display_charset=utf8'
        cmd = [LYNX_BIN, ] + lynx_args.split(' ')
        lynx = subprocess.Popen(cmd, stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE)
        lynx.stdin.write(html.encode('utf8'))
        lynx.stdin.close()
        _t = threading.Timer(200.0, kill_lynx, args=[lynx.pid])
        _t.start()
        text = lynx.stdout.read().decode('utf-8', 'replace')
        _t.cancel()
        return text


class InscriptisHtmlConverter(AbstractHtmlConverter):
    '''
    Converts HTML to text using Inscriptis.
    '''
    name = 'Inscriptis'

    def __init__(self):
        self.available = 'inscriptis' in sys.modules

    def get_text(self, html):
        return inscriptis.get_text(html)


timestamp = str(datetime.now()).replace(' ', '_').replace(':', '-')\
                                                 .split('.')[0]
benchmarking_results_dir = os.path.join(BENCHMARKING_ROOT,
                                        'benchmarking_results', timestamp)
CACHE_DIR = os.path.join(BENCHMARKING_ROOT, 'html_cache')


def save_to_file(algorithm, url, data):
    '''
    Saves a benchmarking result to the given file.
    '''
    result_file = os.path.join(benchmarking_results_dir,
                               '{}_{}.txt'.format(algorithm, url))
    with open(result_file, 'w') as output_file:
        output_file.write(data)


def get_speed_table(times):
    '''
    Provides the table which compares the conversion speed.
    '''
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
            difference = '-{}'.format(difference)
        elif difference == 0:
            difference = '--> fastest'

        output = '{}{}: {}{} {}'.format(key, ' ' * (longest_key - len(key)),
                                        value, ' ' * (longest_value -
                                                      len(str(value))),
                                        difference)
        result += output + '\n'

    return result


def get_fname(url):
    '''
    Transforms a URL to a file name.
    '''
    trash = (('http://', ''),
             ('https://', ''),
             ('/', '-'),
             (':', '-'),
             ('%', ''))

    for key, value in trash:
        url = url.replace(key, value)
    return url[0:100]


CONVERTER = (BeautifulSoupHtmlConverter(),
             JustextHtmlConverter(),
             Html2TextConverter(),
             LynxHtmlConverter(),
             InscriptisHtmlConverter())


def benchmark():
    '''
    Runs the benchmark.
    '''
    # These are a few predefined urls the script will
    with open(os.path.join(BENCHMARKING_ROOT, 'url_list.txt')) as url_list:
        sources = [url.strip() for url in url_list]

    if not os.path.exists(benchmarking_results_dir):
        os.makedirs(benchmarking_results_dir)

    if not os.path.exists(CACHE_DIR):
        os.makedirs(CACHE_DIR)

    for source in sources:
        source_name = get_fname(source)
        source_cache_path = os.path.join(CACHE_DIR, source_name)
        if os.path.exists(source_cache_path):
            html = open(source_cache_path).read()
        else:
            req = urllib.request.Request(source)
            try:
                html = urllib.request.urlopen(req).read().decode('utf-8')
            except UnicodeDecodeError:
                html = urllib.request.urlopen(req).read().decode('latin1')
            open(source_cache_path, 'w').write(html)

        with open(os.path.join(benchmarking_results_dir,
                               'speed_comparisons.txt'), 'a') as output_file:
            output_file.write('\nURL: {}\n'.format(source_name))
        print('\nURL: {}'.format(source_name))

        times = {}
        for converter in CONVERTER:
            if converter.available:
                time_required, text = converter.benchmark(html)
                times[converter.name] = time_required
                save_to_file(converter.name, source_name, text)

        speed_table = get_speed_table(times)
        print(speed_table)

        with open(os.path.join(benchmarking_results_dir,
                               OUTFILE), 'a') as output_file:
            output_file.write(speed_table + '\n')

    with open(os.path.join(benchmarking_results_dir,
                           OUTFILE), 'a') as output_file:
        output_file.write('\n')


if __name__ == '__main__':
    benchmark()
