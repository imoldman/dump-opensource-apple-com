#!/usr/bin/env python

from cStringIO import StringIO
import urllib2
import tarfile
import os
import re
import sys

URL_ROOT = 'http://www.opensource.apple.com/tarballs'
FOLDER_IMG = '/static/images/icons/folder.png'
GZ_IMG = '/static/images/icons/gz.png'
BACK_IMG = '/icons/back.gif'
HREF_RE = re.compile(r'<td[^>]*><a href=\"([^"]+)\"><img[^>]+src="([^"]+)"[^>]*></a></td>')
RESULT_FILE = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'result.txt'), 'w')

def get_content_from_remote(path):
  print 'downloading content from %s ... ' % path
  url = '%s%s' % (URL_ROOT, path)
  request = urllib2.Request(url)
  return urllib2.urlopen(request).read()

def get_html_content(path):
  return get_content_from_remote(path)

def get_tar_gz_file(path):
  content = get_content_from_remote(path)
  return tarfile.open(fileobj=StringIO(content))

def dump_gz_file(path):
  tarfile = get_tar_gz_file(path)
  names = tarfile.getnames()
  for name in names:
    print >> RESULT_FILE, path + '/' + name

def recursive_dump_file_on_html(path):
  content = get_html_content(path)
  for match in HREF_RE.finditer(content):
    href = match.group(1)
    type = match.group(2)
    if type == BACK_IMG:
      continue			# ignore Parent Directory
    new_path = path + href
    if type == FOLDER_IMG:
      print 'found type: folder, href: %s => %s' % (path, href)
      recursive_dump_file_on_html(new_path)
    elif type == GZ_IMG:
      print 'found type: tar.gz, href: %s => %s' % (path, href)
      dump_gz_file(new_path)
    else:
      print >> sys.stderr, 'unkown type: %s, href: %s => %s' % (type, path, href)

def main():
  recursive_dump_file_on_html('/');

if __name__ == '__main__':
  main()
