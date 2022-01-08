import paramiko
import time

from paramiko.client import AutoAddPolicy

def connect(server_ip: str, server_port: str, user: str, password: str): 
    '''SSHサーバに接続'''
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(AutoAddPolicy())
    print(f'Connecting to {server_ip}')
    ssh_client.connect(
        hostname=server_ip, 
        port=server_port,
        username=user,
        password=password,
        look_for_keys=False,
        allow_agent=False
    )
    return ssh_client

def get_shell(ssh_client):
    '''対話型シェルを返す'''
    shell = ssh_client.invoke_shell()
    return shell

def send_command(shell, command: str, timeout=1):
    '''コマンドを実行'''
    print(f'Sending command: {command}')
    shell.send(command + '\n')
    time.sleep(timeout)

def show(shell, n=10000):
    '''結果をデコードして返す'''
    # 結果をバイト列で取得
    output = shell.recv(n)
    return output.decode()

def close(ssh_client):
    '''SSH接続を閉じる'''
    if ssh_client.get_transport().is_active() == True:
        print('Closing the connection')
        ssh_client.close()
