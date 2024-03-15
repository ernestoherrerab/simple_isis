import yaml
from pathlib import Path

def load_yaml(file_path):
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)
    return data

### VARS
dns_hosts_file = Path("/etc/hosts")
topology_yml_file = Path("playbooks/Ernesto_Simple_ISIS.yml")
inventory_yml_file = Path("hosts.yml")
topology_dict = load_yaml(topology_yml_file)
inventory_dict = load_yaml(inventory_yml_file)
cvp_ip = topology_dict["all"]["children"]["CVP"]["hosts"]["cv_server"]["ansible_host"]

### UPDATE LOCAL DNS HOSTS FILE
print("Updating Local DNS Hosts File")
with open(dns_hosts_file, 'w') as file:
    file.write(f'# Host Database\n')
    file.write(f'#\n')
    file.write(f'# localhost is used to configure the loopback interface\n')
    file.write(f'# when the system is booting.  Do not change this entry.\n')
    file.write(f'##\n')
    file.write(f'127.0.0.1\t\tlocalhost\n')
    file.write(f'255.255.255.255\tbroadcasthost\n')
    file.write(f'::1\t\t\t\tlocalhost\n\n\n')
    file.write(f'{cvp_ip}\t\tcvp\n')
    for key, value in topology_dict["all"]["children"]["VEOS"]["hosts"].items():
        file.write(f'{value["ansible_host"]}\t\t{key}\n')

### UPDATE HOSTS FILE WITH CVP NEW IP
print("Updating Inventory")
inventory_dict["all"]["children"]["cvp"]["hosts"]["cv_server"]["ansible_httpapi_host"] = cvp_ip
inventory_dict["all"]["children"]["cvp"]["hosts"]["cv_server"]["ansible_host"] = cvp_ip
with open(inventory_yml_file, 'w') as file:
    yaml.dump(inventory_dict, file, indent=2)