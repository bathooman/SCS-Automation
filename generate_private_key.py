import math
import os

def make_dir(address):
    if not os.path.exists(address):
        try:
            os.makedirs(address)
            print(f'[-] Directory {address} is generated successfully\n')
        except OSError as err:
            print(f"[-] Directory {address} cannot be generated\n")
    else:
        print(f"[-] Directory {address} already exists\n")

def main():
    if os.path.isfile('registered.txt'):
        make_dir("keys")
        f = open('registered.txt', 'r')
        users = f.readlines()
        num_lines = sum(1 for line in open('registered.txt'))
        even_distribution = math.floor(num_lines/5)
        cluster_id = 1
        port_counter = 0
        counter = 0
        for element in users:
            name = str(element).strip()
            make_dir(f"keys/{name}")
            os.system(f"ssh-keygen -f keys/{name}/{name} -t rsa -q -N \"\" -C {name}.key")
            if counter <= even_distribution:
                print(f'name:{name}')
                if cluster_id == 1:
                    with open(f'keys/{name}/{name}.bashrc', 'w') as f:
                        f.write('export JANUS_IP="130.238.10.236"\n')
                        f.write('export KALI_IP="10.11.11.131"\n')
                        f.write(f'export PORT_FROM="{3001 + port_counter}"\n')
                        f.write(f'export PORT_TO="{3001 + port_counter + 4 }"\n')
                        f.write('export MSP_IP="192.168.1.200"\n')
                    counter += 1
                    port_counter += 4
                elif cluster_id == 2:
                    with open(f'keys/{name}/{name}.bashrc', 'w') as f:
                        f.write('export JANUS_IP="130.238.10.236"\n')
                        f.write('export KALI_IP="10.11.11.132"\n')
                        f.write(f'export PORT_FROM="{3001 + port_counter}"\n')
                        f.write(f'export PORT_TO="{3001 + port_counter + 4 }"\n')
                        f.write('export MSP_IP="192.168.2.200"\n')
                    counter += 1
                    port_counter += 4
                elif cluster_id == 3:
                    with open(f'keys/{name}/{name}.bashrc', 'w') as f:
                        f.write('export JANUS_IP="130.238.10.236"\n')
                        f.write('export KALI_IP="10.11.11.133"\n')
                        f.write(f'export PORT_FROM="{3001 + port_counter}"\n')
                        f.write(f'export PORT_TO="{3001 + port_counter + 4}"\n')
                        f.write('export MSP_IP="192.168.3.200"\n')
                    counter += 1
                    port_counter += 4
                elif cluster_id == 4:
                    with open(f'keys/{name}/{name}.bashrc', 'w') as f:
                        f.write('export JANUS_IP="130.238.10.236"\n')
                        f.write('export KALI_IP="10.11.11.134"\n')
                        f.write(f'export PORT_FROM="{3001 + port_counter}"\n')
                        f.write(f'export PORT_TO="{3001 + port_counter + 4}"\n')
                        f.write('export MSP_IP="192.168.4.200"\n')
                    counter += 1
                    port_counter += 4
                elif cluster_id == 5:
                    with open(f'keys/{name}/{name}.bashrc', 'w') as f:
                        f.write('export JANUS_IP="130.238.10.236"\n')
                        f.write('export KALI_IP="10.11.11.136"\n')
                        f.write(f'export PORT_FROM="{3001 + port_counter}"\n')
                        f.write(f'export PORT_TO="{3001 + port_counter + 4}"\n')
                        f.write('export MSP_IP="192.168.6.200"\n')
                    counter += 1
                    port_counter += 4
            elif counter > even_distribution:
                counter = 0
                cluster_id += 1
                if cluster_id == 2:
                    with open(f'keys/{name}/{name}.bashrc', 'w') as f:
                        f.write('export JANUS_IP="130.238.10.236"\n')
                        f.write('export KALI_IP="10.11.11.132"\n')
                        f.write(f'export PORT_FROM="{3001 + port_counter}"\n')
                        f.write(f'export PORT_TO="{3001 + port_counter + 4 }"\n')
                        f.write('export MSP_IP="192.168.2.200"\n')
                    port_counter += 4
                elif cluster_id == 3:
                    with open(f'keys/{name}/{name}.bashrc', 'w') as f:
                        f.write('export JANUS_IP="130.238.10.236"\n')
                        f.write('export KALI_IP="10.11.11.133"\n')
                        f.write(f'export PORT_FROM="{3001 + port_counter}"\n')
                        f.write(f'export PORT_TO="{3001 + port_counter + 4}"\n')
                        f.write('export MSP_IP="192.168.3.200"\n')
                    port_counter += 4
                elif cluster_id == 4:
                    with open(f'keys/{name}/{name}.bashrc', 'w') as f:
                        f.write('export JANUS_IP="130.238.10.236"\n')
                        f.write('export KALI_IP="10.11.11.134"\n')
                        f.write(f'export PORT_FROM="{3001 + port_counter}"\n')
                        f.write(f'export PORT_TO="{3001 + port_counter + 4}"\n')
                        f.write('export MSP_IP="192.168.4.200"\n')
                    port_counter += 4
                elif cluster_id == 5:
                    with open(f'keys/{name}/{name}.bashrc', 'w') as f:
                        f.write('export JANUS_IP="130.238.10.236"\n')
                        f.write('export KALI_IP="10.11.11.136"\n')
                        f.write(f'export PORT_FROM="{3001 + port_counter}"\n')
                        f.write(f'export PORT_TO="{3001 + port_counter + 4}"\n')
                        f.write('export MSP_IP="192.168.6.200"\n')
                    port_counter += 4

def modify_bashrc(group_file):
    if os.path.isfile(group_file):
        f = open(group_file, 'r')
        users = f.readlines()
        number_of_groups = 0
        for user in users:
            if user[0].isdigit():
                number_of_groups += 1

        even_distribution = math.floor(number_of_groups / 5)
        cluster_id = 1
        counter = 0
        port_counter = 0
        for user in users:
            user = user.strip()
            if user[0].isdigit():
                counter += 1
                if counter > even_distribution:
                    counter = 0
                    cluster_id += 1
            else:
                if os.path.isfile(f'keys/{user}/{user}.bashrc'):
                    if (cluster_id == 1):
                        with open(f'keys/{user}/{user}.bashrc', 'w') as f:
                            f.write('export JANUS_IP="130.238.10.236"\n')
                            f.write('export KALI_IP="10.11.11.131"\n')
                            f.write(f'export PORT_FROM="{3001 + port_counter}"\n')
                            f.write(f'export PORT_TO="{3001 + port_counter + 4}"\n')
                            f.write('export MSP_IP="192.168.1.200"\n')
                        port_counter += 5
                    elif cluster_id == 2:
                        with open(f'keys/{user}/{user}.bashrc', 'w') as f:
                            f.write('export JANUS_IP="130.238.10.236"\n')
                            f.write('export KALI_IP="10.11.11.132"\n')
                            f.write(f'export PORT_FROM="{3001 + port_counter}"\n')
                            f.write(f'export PORT_TO="{3001 + port_counter + 4}"\n')
                            f.write('export MSP_IP="192.168.2.200"\n')
                        port_counter += 5
                    elif cluster_id == 3:
                        with open(f'keys/{user}/{user}.bashrc', 'w') as f:
                            f.write('export JANUS_IP="130.238.10.236"\n')
                            f.write('export KALI_IP="10.11.11.133"\n')
                            f.write(f'export PORT_FROM="{3001 + port_counter}"\n')
                            f.write(f'export PORT_TO="{3001 + port_counter + 4}"\n')
                            f.write('export MSP_IP="192.168.3.200"\n')
                        port_counter += 5
                    elif cluster_id == 4:
                        with open(f'keys/{user}/{user}.bashrc', 'w') as f:
                            f.write('export JANUS_IP="130.238.10.236"\n')
                            f.write('export KALI_IP="10.11.11.134"\n')
                            f.write(f'export PORT_FROM="{3001 + port_counter}"\n')
                            f.write(f'export PORT_TO="{3001 + port_counter + 4}"\n')
                            f.write('export MSP_IP="192.168.4.200"\n')
                        port_counter += 5
                    elif cluster_id == 5:
                        with open(f'keys/{user}/{user}.bashrc', 'w') as f:
                            f.write('export JANUS_IP="130.238.10.236"\n')
                            f.write('export KALI_IP="10.11.11.136"\n')
                            f.write(f'export PORT_FROM="{3001 + port_counter}"\n')
                            f.write(f'export PORT_TO="{3001 + port_counter + 4}"\n')
                            f.write('export MSP_IP="192.168.6.200"\n')
                        port_counter += 5
                else:
                    print(f"Error:{user}")
                    exit(-1)


        print(number_of_groups)
if __name__ == '__main__':
    # main()
    modify_bashrc('group_members.txt')
