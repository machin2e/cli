import psutil
import netifaces

def kill_proc_tree(pid, including_parent=True):    
    parent = psutil.Process(pid)
    children = parent.children(recursive=True)
    for child in children:
        child.kill()
    gone, still_alive = psutil.wait_procs(children, timeout=5)
    if including_parent:
        parent.kill()
        parent.wait(5)

def get_inet_addresses():
	addresses = []
	for iface_name in netifaces.interfaces():
		#iface_addresses = [i['addr'] for i in netifaces.ifaddresses(ifaceName).setdefault(netifaces.AF_INET, [{'addr': 'No IP addr'}])]
		#iface_addresses = [i['addr'] for i in netifaces.ifaddresses(iface_name).setdefault(netifaces.AF_INET, [{'addr': None}])]
		for i in netifaces.ifaddresses(iface_name).setdefault(netifaces.AF_INET, [{'addr': None}]):
			if not i['addr'] == None:
				addresses.append(i['addr'])
	return addresses
