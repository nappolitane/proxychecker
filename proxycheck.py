import requests
import threading
import argparse
import json
import sys
import os

file_lock = threading.Lock()
list_parsed = 0

def check_proxies(proxy_list, outp_dir, proxy_type, start, end):
	global file_lock
	global list_parsed
	for proxy_line in proxy_list[start:end]:
		proxs = {"http": proxy_line, "https": proxy_line}
		try:
			r = requests.get("http://ipinfo.io", proxies=proxs)
			json_data = json.loads(r.text)
			with file_lock:
				list_parsed += 1
				with open(outp_dir + "/" + proxy_type + "_" + json_data["country"] + ".txt", 'a') as outfile:
					outfile.write(proxy_line + '\r\n')
		except requests.exceptions.ConnectionError:
			pass
		except json.decoder.JSONDecodeError:
			pass
		except Exception as err:
			print(f"Unexpected {err=}, {type(err)=}")
			pass

if __name__ =="__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('-i', '--inputfile', help='Input file name', required=True)
	parser.add_argument('-p', '--proxytype', help='Proxy type', required=True)
	parser.add_argument('-t', '--threadsnum', help='Number of threads', required=True)
	parser.add_argument('-o', '--outputdir', help='Output directory', required=True)
	args = parser.parse_args()
	
	if not os.path.isdir(args.outputdir):
		sys.exit("Output directory does not exist")
	
	proxy_list = []
	with open(args.inputfile, 'r') as infile:
		for line in infile:
			proxy_line = args.proxytype + "://" + line.strip()
			proxy_list.append(proxy_line)
	
	nr_threads = int(args.threadsnum)
	threads = []
	for i in range(nr_threads):
		start = i * (len(proxy_list) // nr_threads)
		end = (i + 1) * (len(proxy_list) // nr_threads) if i < nr_threads - 1 else len(proxy_list)
		t = threading.Thread(target=check_proxies, args=(proxy_list,args.outputdir,args.proxytype,start,end,))
		t.start()
		threads.append(t)
	
	aux = list_parsed
	while list_parsed < (len(proxy_list) // nr_threads):
		if list_parsed != aux:
			print("{} %  ".format(round(list_parsed / (len(proxy_list) // nr_threads) * 100, 2)), end='\r', flush=True)
			sys.stdout.flush()
			aux = list_parsed
	
	for thread in threads:
		thread.join()

