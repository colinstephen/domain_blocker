#!/usr/bin/env python

'''
Append new domain blocks to the system hosts file.
This script must be run with root privileges to work.
'''

import argparse

HOSTS = '/etc/hosts'  # default hosts file

def parse_hosts(hosts_file):
	'''
	Return a list of currently blocked URLs.
	'''

	with open(hosts_file, 'r') as f:
		lines = [line.strip() for line in f.readlines()]

	urls = [line.split()[1] for line in lines if line.startswith('127.0.0.1')]
	
	return urls


def parse_from(from_file):
	'''
	Return a list of URLs read from a text file (first column).
	'''

	with open(from_file, 'r') as f:
		lines = [line.strip() for line in f.readlines()]

	urls = [line.split()[0] for line in lines
			  if not line.startswith('#') and '.' in line]

	return urls


def get_difference(old_list, new_list):
	'''
	Return elements that are in new list but not in old list.
	'''

	diff = [el for el in new_list if el not in old_list]

	return diff


def add_www(urls):
	'''
	Expand a list of URLs by including the 'www' version if not already present.
	'''

	www = lambda u: 'www.{}'.format(u)
	wwws = [www(url) for url in urls if www(url) not in urls]
	urls = urls + wwws

	return urls


def append_lines(lines, to_file):
	'''
	Append a list of lines to a file.
	'''

	with open(to_file, 'a') as f:
		f.writelines(lines)

	return None


def append_blocks(from_file, hosts_file=HOSTS):
	'''
	Parse the given source and hosts files and append blocks to the hosts file,
	for each new URL in the source file.
	'''

	source_urls = parse_from(from_file)
	#print('source_urls:', source_urls)
	
	hosts_urls = parse_hosts(hosts_file)
	#print('hosts_urls:', hosts_urls)
	
	new_domains = get_difference(hosts_urls, source_urls)
	#print('new_domains:', new_domains)
	
	urls_to_add = add_www(new_domains)
	#print('urls_to_add:', urls_to_add)
	
	lines_to_add = ['127.0.0.1 {}\n'.format(url) for url in urls_to_add]
	#print('lines_to_add:', lines_to_add)

	append_lines(lines_to_add, hosts_file)

	if len(lines_to_add) > 0:
		print('Added lines:\n\n{}\n'.format('\n'.join(lines_to_add)))
	else:
		print('No new domains to add.')

	return None


def main():
	'''
	Parse the command line arguments and pass them to the worker function.
	'''

	parser = argparse.ArgumentParser(
		description="Append new URL blocks to the system hosts file.")
	parser.add_argument('-from_file', required=True,
		help='File containing new URLs to append to hosts.')
	parser.add_argument('-hosts_file', default=HOSTS,
		help='System hosts file (default {}).'.format(HOSTS))
	
	args = parser.parse_args()
	from_file = args.from_file
	hosts_file = args.hosts_file

	try:
		append_blocks(from_file, hosts_file=hosts_file)
		print('Successfully added blocks to hosts file {}'.format(hosts_file))
	except Exception as e:
		print('Error writing blocks to hosts file {}'.format(hosts_file))
		print(e)

	return None


if __name__ == '__main__':
	main()