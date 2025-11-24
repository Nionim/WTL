import paramiko, os
from scp import SCPClient
from dotenv import load_dotenv
import traceback

load_dotenv()
ssh_port = int(os.getenv("ssh_port"))
ssh_host = os.getenv("ssh_host")
ssh_user = os.getenv("ssh_user")
ssh_key = os.getenv("ssh_key")

def getClient():
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=ssh_host, port=ssh_port, username=ssh_user, key_filename=ssh_key)
        return client
    except Exception as e:
        print(f"Ssh failed: {type(e).__name__}: {e}")
        return None

def runCommand(command):
    try:
        client = getClient()
        stdin, stdout, stderr = client.exec_command(command)
        print(f"Command ({command}) out: {stdout}")

        e = stderr.read().decode()
        if e: print(f"Executing error: {e}")
        else: print(f"{command} Executed!")
    except Exception as e:
        if e: print(f"Executing error for {command}: {e}")
    finally: client.close()

def editFile(localPath, remotePath):
    try:
        client = getClient()
        with SCPClient(client.get_transport()) as scp:
            scp.put(localPath, remotePath)
            print(f"File {localPath} successfully moved to {remotePath}!")
    except Exception as e:
        print(f"Moving error for {localPath}: {e}")
    finally: client.close()

def deleteFile(remotePath):
    try:
        client = getClient()
        stdin, stdout, stderr = client.exec_command(f"rm -f {remotePath}")

        e = stderr.read().decode()
        if e: print(f"Deleting error: {e}")
        else: print(f"File {remotePath} successfully moved!")
    except Exception as e:
        if e: print(f"Deleting error for {remotePath}: {e}")
    finally: client.close()