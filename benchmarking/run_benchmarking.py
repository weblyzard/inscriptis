#!/usr/bin/env python3
"""Run a benchmarking suite to compare speed and output of different implementations."""

import argparse
import operator
import os
import signal
import subprocess
import sys
import threading
import urllib.request
from datetime import datetime
from time import time

#
# Import inscriptis (using the version in the project directory rather than
# any installed module versions).
#

LYNX_BIN = "/usr/bin/lynx"
LINKS_BIN = "/usr/bin/links"
BENCHMARKING_ROOT = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(BENCHMARKING_ROOT, "../src")
sys.path.insert(0, os.path.abspath(SRC_DIR))

try:
    import inscriptis
except ImportError:
    print("Inscriptis is not available. Please install it in order to compare with inscriptis.")

#
# Import third-party HTML 2 text converters.
#
try:
    from bs4 import BeautifulSoup
except ImportError:
    print("BeautifulSoup is not available. Please install it in order to compare with BeautifulSoup.")
try:
    import html2text
except ImportError:
    print("html2text is not available. Please install it in order to compare with html2text.")
try:
    import justext
except ImportError:
    print("justext is not available. Please install it in order to compare with justext.")


TRIES = 7
OUTFILE = "speed_comparisons.txt"


class AbstractHtmlConverter:
    """An abstract HTML convert class."""

    def get_text(self, html):
        """Return a text representation of the given HTML snippet."""
        raise NotImplementedError

    def benchmark(self, html):
        """Benchmarks the classes HTML to text converter.

        Return a tuple of the required time and the obtained text representation.
        """
        start_time = time()
        for _ in range(TRIES):
            text = self.get_text(html)
        return time() - start_time, text


class BeautifulSoupHtmlConverter(AbstractHtmlConverter):
    """Converts HTML to text using BeautifulSoup."""

    name = "BeautifulSoup"

    def __init__(self):
        self.available = "bs4" in sys.modules

    def get_text(self, html):
        soup = BeautifulSoup(html, "lxml")

        for script in soup(["script", "style"]):
            script.extract()

        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        return "\n".join(chunk for chunk in chunks if chunk)


class JustextConverter(AbstractHtmlConverter):
    """Converts HTML to text using Justtext."""

    name = "Justtext"

    def __init__(self):
        self.available = "justext" in sys.modules

    def get_text(self, html):
        paragraphs = justext.justext(html, stoplist="English")
        result = [paragraph.text for paragraph in paragraphs]
        return "\n".join(result)


class Html2TextConverter(AbstractHtmlConverter):
    """Converts HTML to text using Html2Text."""

    name = "Html2Text"

    def __init__(self):
        self.available = "html2text" in sys.modules

    def get_text(self, html):
        converter = html2text.HTML2Text()
        converter.ignore_links = True
        result = converter.handle(str(html))
        return "".join(result)


class LynxConverter(AbstractHtmlConverter):
    """Converts HTML to text using lynx."""

    name = "Lynx"

    def __init__(self):
        try:
            subprocess.call([LYNX_BIN, "-dump 'www.google.com'"], stdout=subprocess.PIPE)
            self.available = True
        except OSError:
            print("lynx can not be called. Please check in order to compare with lynx.")
            self.available = False

    def get_text(self, html):
        def kill_lynx(pid):
            os.kill(pid, signal.SIGKILL)
            os.waitpid(-1, os.WNOHANG)
            print("lynx killed")

        lynx_args = "-stdin -width=20000 -force_html -nocolor -dump -nolist -nobold -display_charset=utf8"
        cmd = [LYNX_BIN, *lynx_args.split(" ")]
        lynx = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        lynx.stdin.write(html.encode("utf8"))
        lynx.stdin.close()
        _t = threading.Timer(200.0, kill_lynx, args=[lynx.pid])
        _t.start()
        text = lynx.stdout.read().decode("utf-8", "replace")
        _t.cancel()
        return text


class LinksConverter(AbstractHtmlConverter):
    """Converts HTML to text using links."""

    name = "Links"

    def __init__(self):
        try:
            subprocess.call([LINKS_BIN, "-dump 'www.google.com'"], stdout=subprocess.PIPE)
            self.available = True
        except OSError:
            print("links can not be called. Please check in order to compare with links.")
            self.available = False

    def get_text(self, html):
        def kill_links(pid):
            os.kill(pid, signal.SIGKILL)
            os.waitpid(-1, os.WNOHANG)
            print("links killed")

        links_args = "-dump "
        cmd = [LINKS_BIN, *links_args.split(" ")]
        links = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        links.stdin.write(html.encode("utf8"))
        links.stdin.close()
        _t = threading.Timer(200.0, kill_links, args=[links.pid])
        _t.start()
        text = links.stdout.read().decode("utf-8", "replace")
        _t.cancel()
        return text


class InscriptisHtmlConverter(AbstractHtmlConverter):
    """Converts HTML to text using Inscriptis."""

    name = "Inscriptis"

    def __init__(self):
        self.available = "inscriptis" in sys.modules
        if self.available:
            self.get_text = inscriptis.get_text


timestamp = str(datetime.now()).replace(" ", "_").replace(":", "-").split(".")[0]
DEFAULT_RESULT_DIR = os.path.join(BENCHMARKING_ROOT, "benchmarking_results", timestamp)
DEFAULT_CACHE_DIR = os.path.join(BENCHMARKING_ROOT, "html_cache")


def save_to_file(algorithm, url, data, benchmarking_results_dir):
    """Save the benchmarking result to the given file."""
    result_file = os.path.join(benchmarking_results_dir, f"{algorithm}_{url}.txt")
    with open(result_file, "w") as output_file:
        output_file.write(data)


def get_speed_table(times):
    """Provide the table which compares the conversion speed."""
    fastest = min((value for _, value in times.items()))
    longest_key = max(len(key) for key, _ in times.items())
    longest_value = max(len(str(value)) for _, value in times.items())

    result = ""
    for key, value in sorted(times.items(), key=operator.itemgetter(1)):
        difference = value - fastest
        difference = "--> fastest" if difference == 0 else f"{difference:+f}"

        output = "{}{}: {}{} {}".format(
            key,
            " " * (longest_key - len(key)),
            value,
            " " * (longest_value - len(str(value))),
            difference,
        )
        result += output + "\n"

    return result


def get_fname(url) -> str:
    """Transform a URL to a file name."""
    trash = (("http://", ""), ("https://", ""), ("/", "-"), (":", "-"), ("%", ""))

    for key, value in trash:
        url = url.replace(key, value)
    return url[0:100]


CONVERTER = (
    BeautifulSoupHtmlConverter(),
    JustextConverter(),
    Html2TextConverter(),
    LynxConverter(),
    LinksConverter(),
    InscriptisHtmlConverter(),
)


def parse_args():
    """Parse optional benchmarking arguments."""
    parser = argparse.ArgumentParser(description="Inscriptis benchmarking suite")
    parser.add_argument(
        "converter",
        type=str,
        nargs="*",
        help="The list of converters to benchmark (options:"
        "BeautifulSoup, Justext, Html2Text, Lynx, "
        "Inscriptis; default: all)",
    )
    parser.add_argument(
        "-u",
        "--benchmarking-urls",
        default=os.path.join(BENCHMARKING_ROOT, "url_list.txt"),
        help="A list of URLs to use in the benchmark.",
    )
    parser.add_argument(
        "-r",
        "--benchmarking-results",
        default=DEFAULT_RESULT_DIR,
        help="Optional directory for saving the benchmarking results.",
    )
    parser.add_argument(
        "-c",
        "--cache",
        default=DEFAULT_CACHE_DIR,
        help="Optional cache directory for the retrieved Web pages.",
    )
    return parser.parse_args()


def _setup_benchmarking_directories(args):
    """Set up the benchmarking result and caching directories.

    Args:
        args: command line arguments that provide the directory names.

    """
    if not os.path.exists(args.benchmarking_results):
        os.makedirs(args.benchmarking_results)
    if not os.path.exists(args.cache):
        os.makedirs(args.cache)


def _fetch_url(url, cache_dir):
    """Fetch the given URL either from the cache or from the Web.

    URLs that are not yet cached are added to the cache.

    Args:
        url: the URL to fetch.
        cache_dir: the cache directory.

    Returns:
        A tuple of the cache file name and the URLs content.

    """
    source_name = get_fname(url)
    source_cache_path = os.path.join(cache_dir, source_name)

    if os.path.exists(source_cache_path):
        with open(source_cache_path) as f:
            html = f.read()
    else:
        req = urllib.request.Request(url)
        try:
            html = urllib.request.urlopen(req).read().decode("utf-8")
        except UnicodeDecodeError:
            html = urllib.request.urlopen(req).read().decode("latin1")
        with open(source_cache_path, "w") as f:
            f.write(html)

    return source_name, html


def benchmark(args, source_list):
    """Run the benchmark.

    Args:
        args: command line arguments
        source_list: a list of URLs to benchmark.

    """
    _setup_benchmarking_directories(args)

    output = []
    total_times = {}
    for source in source_list:
        source_name, html = _fetch_url(source, args.cache)

        print(f"\nURL: {source_name}")
        output.append(f"\nURL: {source_name}\n")

        times = {}
        for converter in CONVERTER:
            if (converter.available and not args.converter) or converter.name in args.converter:
                time_required, text = converter.benchmark(html)
                times[converter.name] = time_required
                save_to_file(converter.name, source_name, text, args.benchmarking_results)

        for converter, conversion_time in times.items():
            total_times[converter] = total_times.get(converter, 0) + conversion_time
        speed_table = get_speed_table(times)
        print(speed_table)
        output.append(speed_table)

    print("\nTotal")
    output.append("\nTotal\n")
    speed_table = get_speed_table(total_times)
    print(speed_table)
    output.append(speed_table)

    with open(os.path.join(args.benchmarking_results, OUTFILE), "w") as output_file:
        output_file.write("\n".join(output) + "\n")


if __name__ == "__main__":
    # These are a few predefined urls the script will
    cmdline_args = parse_args()
    with open(cmdline_args.benchmarking_urls) as url_list:
        sources = [url.strip() for url in url_list]

    benchmark(cmdline_args, sources)
