import paramiko, os
from scp import SCPClient
from dotenv import load_dotenv

load_dotenv()
ssh_host = os.getenv("ssh_host")
ssh_user = os.getenv("ssh_user")
ssh_key = os.getenv("ssh_key")

def getClient():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=ssh_host, username=ssh_user, key_filename=ssh_key)
    return client

def editFile(localPath, remotePath):
    try:
        client = getClient()
        with SCPClient(client.get_transport()) as scp:
            scp.put(localPath, remotePath)
            print(f"File {localPath} successfully moved to {remotePath}!")
    except Exception as e:
        print(f"Moving error: {e}")
    finally: client.close()

def deleteFile(remotePath):
    try:
        client = getClient()
        stdin, stdout, stderr = client.exec_command(f"rm -f {remotePath}")

        e = stderr.read().decode()
        if e: print(f"Deleting error: {e}")
        else: print(f"File {remotePath} successfully moved!")
    except Exception as e:
        if e: print(f"Deleting error: {e}")
    finally: client.close()