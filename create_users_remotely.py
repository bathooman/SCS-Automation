import argparse
import os
import sys
import paramiko



def get_arguments():
    passwd = ""
    arg_parser = argparse.ArgumentParser(description="The program gets a file containing the names for registered "
                                                     "users and create users for them on the SSH Server")

    arg_parser.add_argument("-u", "--username", type=str, required=True, help="The username on the SSH server")
    arg_parser.add_argument("-p", "--password_file", type=str, required=True, help="The file containing the password "
                                                                                   "to access your private key")
    arg_parser.add_argument("-i", "--input_file", type=str, required=True, help="The address to the file"
                                                                                "containing the student's names for "
                                                                                "Canvas")
    args = arg_parser.parse_args()

    if not (os.path.isfile(args.password_file)):
        print("Invalid path for the token file")
        sys.exit(2)

    with open(os.path.abspath(args.password_file)) as f:
        passwd = f.readline().strip()

    return args.username, passwd, args.input_file

def run_command(ssh_client, cmd):
    stdin, stdout, stderr = ssh_client.exec_command(cmd, get_pty=True)
    out = stdout.read().decode().strip()
    error = stderr.read().decode().strip()
    if out is not None:
        print(out)
    if error:
        raise Exception('There was an error pulling the runtime: {}'.format(error))

def create_users(username, password, input_file):
    if os.path.isfile(input_file):
        ssh = paramiko.SSHClient()
        pkey = paramiko.RSAKey.from_private_key_file("/home/hooman/.ssh/id_rsa", password=password)
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname='130.238.10.236', username=username, pkey=pkey)
        f = open(input_file, 'r')
        users = f.readlines()
        for element in users:
            name = str(element).strip()
            run_command(ssh, f"sudo useradd {name}")
            run_command(ssh, f"sudo mkdir /home/{name}/.ssh")
            run_command(ssh, f"sudo chmod 700 /home/{name}/.ssh")
            run_command(ssh, f"sudo touch /home/{name}/.ssh/authorized_keys")
            run_command(ssh, f"sudo chmod 600 /home/{name}/.ssh/authorized_keys")
            with open(f'keys/{name}/{name}.pub', 'r') as f:
                publickey = str(f.readline())
                run_command(ssh, f'''sudo sh -c "echo '{publickey}' >> /home/{name}/.ssh/authorized_keys"''')
            with open(f'keys/{name}/{name}.bashrc', 'r') as f:
                lines = f.readlines()
                for line in lines:
                    run_command(ssh, f'''sudo sh -c "echo '{line}' >> /home/{name}/.bashrc"''')
            run_command(ssh, f"sudo chown {name} /home/{name}/.ssh")
            run_command(ssh, f"sudo chown {name} /home/{name}/.ssh/authorized_keys")


def delete_users(username, password, input_file):
    if os.path.isfile(input_file):
        ssh = paramiko.SSHClient()
        pkey = paramiko.RSAKey.from_private_key_file("/home/hooman/.ssh/id_rsa", password=password)
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname='130.238.10.236', username=username, pkey=pkey)
        f = open(input_file, 'r')
        users = f.readlines()
        for element in users:
            name = str(element).strip()
            run_command(ssh, f"sudo killall -u {name}")
            run_command(ssh, f"sudo userdel {name}")
            run_command(ssh, f"sudo rm -rf /home/{name}")

def update_bashrc(username, password, input_file):
    if os.path.isfile(input_file):
        ssh = paramiko.SSHClient()
        pkey = paramiko.RSAKey.from_private_key_file("/home/hooman/.ssh/id_rsa", password=password)
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname='130.238.10.236', username=username, pkey=pkey)
        f = open(input_file, 'r')
        users = f.readlines()
        for element in users:
            name = str(element).strip()
            run_command(ssh, f'''sudo cp .bashrc /home/{name}/.bashrc''')
            with open(f'keys/{name}/{name}.bashrc', 'r') as f:
                lines = f.readlines()
                for line in lines:
                    run_command(ssh, f'''sudo sh -c "echo '{line}' >> /home/{name}/.bashrc"''')
def main():
    uname, passwd, input_file = get_arguments()
    # create_users(uname, passwd, input_file)
    # delete_users(uname, passwd, input_file)
    update_bashrc(uname, passwd, input_file)


if __name__ == '__main__':
    main()
