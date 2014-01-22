#!/usr/bin/env python

from cStringIO import StringIO
import urllib2
import tarfile
import os
import re
import sys

URL_ROOT = 'http://www.opensource.apple.com/tarballs/'
FOLDER_IMG = '/static/images/icons/folder.png'
GZ_IMG = '/static/images/icons/gz.png'
BACK_IMG = '/icons/back.gif'
HREF_RE = re.compile(r'<td[^>]*><a href=\"([^"]+)\"><img[^>]+src="([^"]+)"[^>]*></a></td>')
RESULT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'result')
TEMP_RESULT_FILE_NAME = 'result.txt.tmp'
RESULT_FILE_NAME = 'result.txt'

def get_content_from_remote(path):
  url = '%s%s' % (URL_ROOT, path)
  request = urllib2.Request(url)
  return urllib2.urlopen(request).read()

def get_html_content(path):
  return get_content_from_remote(path)

def get_tar_gz_file(path):
  print 'downloading gz from %s ... ' % path
  content = get_content_from_remote(path)
  return tarfile.open(fileobj=StringIO(content))

def make_sure_dir_exists(path):
  full_path = os.path.join(RESULT_DIR, path)
  if not os.path.exists(full_path):
    os.makedirs(full_path)

def is_gz_parse_complete(path):
  full_path  = os.path.join(RESULT_DIR, path, RESULT_FILE_NAME)
  return os.path.exists(full_path)

def get_file_object_to_store_result(path):
  full_directory = os.path.join(RESULT_DIR, path)
  make_sure_dir_exists(full_directory)
  return open(os.path.join(full_directory, TEMP_RESULT_FILE_NAME), 'w')

def mark_gz_parse_complete(path):
  full_path = os.path.join(RESULT_DIR, path, RESULT_FILE_NAME)
  temp_file_path = os.path.join(RESULT_DIR, path, TEMP_RESULT_FILE_NAME)
  os.rename(temp_file_path, full_path)

def dump_gz_file(path):
  result_file = get_file_object_to_store_result(path)
  try:
    tarfile = get_tar_gz_file(path)
    names = tarfile.getnames()
    for name in names:
      print >> result_file, path + '/' + name
  except KeyboardInterrupt:
    raise  # we don't catch ctrl+c
  except:
    print >> sys.stderr, 'unable to untar file: %s' % path

def recursive_dump_file_on_html(path):
  content = get_html_content(path)
  href_and_types  = [(m.group(1), m.group(2)) for m in HREF_RE.finditer(content)];
  total_count = len(href_and_types)
  for index, href_and_type in enumerate(href_and_types):
    href = href_and_type[0]
    type = href_and_type[1]
    if type == BACK_IMG:
      continue			# ignore Parent Directory
    print '(%d/%d), ' % (index, total_count-1),  # ignore Parent Directory
    new_path = path + href
    if type == FOLDER_IMG:
      print 'found type: folder, href: %s => %s' % (path, href)
      recursive_dump_file_on_html(new_path)
    elif type == GZ_IMG:
      print 'found type: tar.gz, href: %s => %s' % (path, href)
      if not is_gz_parse_complete(new_path):
        dump_gz_file(new_path)
        mark_gz_parse_complete(new_path)
    else:
      print >> sys.stderr, 'unkown type: %s, href: %s => %s' % (type, path, href)

def main():
  recursive_dump_file_on_html('./');

if __name__ == '__main__':
  main()
