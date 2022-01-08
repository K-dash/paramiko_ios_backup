import os
import datetime
import threading
import paramiko_mod
from datetime import datetime

def backup(router):
    # sshクライアントを生成
    client = paramiko_mod.connect(**router)

    # 対話型シェルを呼び出す
    shell = paramiko_mod.get_shell(client)

    # ssh接続先で実行するコマンドをシェルに渡す
    paramiko_mod.send_command(shell, 'enable')
    paramiko_mod.send_command(shell, '######') # enableパスワード
    paramiko_mod.send_command(shell, 'terminal length 0')

    # sh runの結果が取得できない場合はtimeout値を調整
    paramiko_mod.send_command(shell, 'sh run', timeout=3)     

    # 結果を取得&リストに整形
    output = paramiko_mod.show(shell)

    # [show run]コマンド 実行結果の不要な箇所を削除するため、一度リストに変換する
    output_list = output.splitlines()
    output_list = output_list[11:-1]

    # リストを文字列に戻す 
    output = '\n'.join(output_list)
    print(output)

    # バックアップ先のディレクトリがなければ作成
    backup_dir = f'backup/{router["server_ip"]}'
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)

    # 結果をバックアップファイルに書き出す
    bk_file_name = f'{router["server_ip"]}_{now.year}{now.month}{now.day}'
    with open(f'{backup_dir}/{bk_file_name}', 'w') as f:
        f.write(output)

    paramiko_mod.close(client)

router1 = {
    'server_ip': '192.168.x.x',
    'server_port': '22',
    'user': 'XXXXXXX',
    'password': 'XXXXXXX'
}
router2 = {
    'server_ip': '192.168.x.y',
    'server_port': '22',
    'user': 'XXXXXXX',
    'password': 'XXXXXXX'
}
router3 = {
    'server_ip': '192.168.x.z',
    'server_port': '22',
    'user': 'XXXXXXX',
    'password': 'XXXXXXX'
}

routers = [router1, router2, router3]

if __name__ == '__main__':

    now = datetime.now()

    # バックアップ関数をスレッドリストに詰める
    threads = [threading.Thread(target=backup, args=(router,)) for router in routers]

    # マルチスレッドでバックアップ開始
    for th in threads:
        th.start()

    # バックアップがすべて終わるまで待機
    for th in threads:
        th.join()
