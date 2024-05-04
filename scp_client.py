import os
import paramiko
from scp import SCPClient, SCPException
from scp_config import HOSTNAME, USERNAME, PASSWORD, LOCAL_PATH, REMOTE_PATH, MATCH_STRING




def delete_file(file_path):
    try:
        os.remove(file_path)
        print(f"File '{file_path}' has been deleted successfully.")
    except FileNotFoundError:
        print(f"The file '{file_path}' does not exist.")
    except PermissionError:
        print(f"Permission denied: unable to delete '{file_path}'.")
    except Exception as e:
        print(f"An error occurred: {e}")

class SSHManager:
    """
    usage:
        >>> import SSHManager
        >>> ssh_manager = SSHManager()
        >>> ssh_manager.create_ssh_client(hostname, username, password)
        >>> ssh_manager.send_command("ls -al")
        >>> ssh_manager.send_file("/path/to/local_path", "/path/to/remote_path")
        >>> ssh_manager.get_file("/path/to/remote_path", "/path/to/local_path")
        ...
        >>> ssh_manager.close_ssh_client()
    """
    def __init__(self):
        self.ssh_client = None

    def create_ssh_client(self, hostname, username, password):
        """Create SSH client session to remote server"""
        if self.ssh_client is None:
            self.ssh_client = paramiko.SSHClient()
            self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh_client.connect(hostname, username=username, password=password, look_for_keys=False)
        else:
            print("SSH client session exist.")

    def close_ssh_client(self):
        """Close SSH client session"""
        self.ssh_client.close()

    def send_file(self, local_path, remote_path, match_file_string):
        """Send a single file to remote path"""
        file_list = os.listdir(local_path)
        file_name = ""
        for i in file_list : 
            if match_file_string in i :
                file_name = i
                break
        if not file_name:
            print("There are no matching files!")
            exit(0)
        local_file_path = f"{local_path}/{file_name}"
        try:
            with SCPClient(self.ssh_client.get_transport()) as scp:
                scp.put(local_file_path, remote_path, preserve_times=True)
        except SCPException:
            raise SCPException.message
        
        return local_file_path

    def get_file(self, remote_path, local_path):
        """Get a single file from remote path"""
        try:
            with SCPClient(self.ssh_client.get_transport()) as scp:
                scp.get(remote_path, local_path)
        except SCPException:
            raise SCPException.message

    def send_command(self, command):
        """Send a single command"""
        stdin, stdout, stderr = self.ssh_client.exec_command(command)
        return stdout.readlines()

def send_file_to_remote() :
    ssh_manager = SSHManager()
    ssh_manager.create_ssh_client(HOSTNAME, USERNAME, PASSWORD) 
    local_file_path = ssh_manager.send_file(LOCAL_PATH, REMOTE_PATH, MATCH_STRING) 
    delete_file(local_file_path)
    ssh_manager.close_ssh_client() 
