#!/usr/bin/env python

import os

ROOT_PATH=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'result')

def remove_if_empty_result(arg, folder, child):
  result = os.path.join(folder, 'result.txt')
  if os.path.exists(result) and os.path.getsize(result) == 0:
    print 'remove %s' % result
    os.remove(result)

def main():
  os.path.walk(ROOT_PATH, remove_if_empty_result, None)

if __name__ == '__main__':
  main()
