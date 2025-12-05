from gpiozero import LED  # gpiozeroモジュールを使用
import time
import subprocess

gpio_led = 14    #gpioピン
led = LED(gpio_led)
tick = 0.075    #短点の長さ[s]
log = False    #ログ(ton, tu)の表示切替

def ton():    #短点を表示
    if log :
        print("ton")
    led.on()
    time.sleep(tick)
    led.off()
    time.sleep(tick * 3)

def tu():    #長点を表示
    if log :
        print("tu")
    led.on()
    time.sleep(tick * 3)
    led.off()
    time.sleep(tick * 3)

morse = {
    "A" : "01",
    "B" : "1000",
    "C" : "1010",
    "D" : "100",
    "E" : "0",
    "F" : "0010",
    "G" : "110",
    "H" : "0000",
    "I" : "00",
    "J" : "0111",
    "K" : "101",
    "L" : "0100",
    "M" : "11",
    "N" : "10",
    "O" : "111",
    "P" : "0110",
    "Q" : "1101",
    "R" : "010",
    "S" : "000",
    "T" : "1",
    "U" : "001",
    "V" : "0001",
    "W" : "011",
    "X" : "1001",
    "Y" : "1011",
    "Z" : "1100"
}

alpha = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

on_list = ["ON", "TRUE", "1"]
off_list = ["OFF", "FALSE", "0"]

# 初期状態表示
print(f"キーボードから入力されたアルファベットの文字列をモールス信号にしてLEDを光らせます")
print(f'/help でコマンド一覧を表示')
print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
print(f'現在の設定')
print(f'GPIOピン    : {gpio_led}番')
print(f'短点の長さ  : {tick}秒')
print(f'ログの表示  : {log}')
print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')

# ループ
while(1 == 1):
    print("morse.py:$ ", end = "")
    str = input()    # 標準入力を受け取る
    str = str.upper()    # 標準入力を大文字に変換

    if str.startswith('/HELP'):
        print()
        print('/exit            : このプログラムを終了')
        print('/info            : 現在の短点の長さとGPIOピンを表示')
        print('/tick [time]     : 短点の長さ[秒]を変更')
        print('/gpio [pin_num]  : GPIOピンを変更')
        print('/log [on / off]  : ログの表示切替' )
        print('/pinout          : raspberry piのGPIOピン情報を表示(pinout)')
        print()
        continue
    if str.startswith('/INFO'):
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        print(f'現在の設定')
        print(f'GPIOピン    : {gpio_led}番')
        print(f'短点の長さ  : {tick}秒')
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        continue
    if str.startswith('/TICK'):
        line = str.split()
        if len(line) == 2:
            line = str.split()
            tick = float(line[1])
            print(f'短点の長さ は {tick}秒 に設定されました')
        else:
            print('引数が不正です\n短点の長さの変更 : /tick [time(s)]')
        continue
    if str.startswith('/GPIO'):
        line = str.split()
        if len(line) == 2:
            gpio_led = line[1]
            print(f'GPIOピンは {gpio_led}番 に設定されました')
        else:
            print('引数が不正です\nGPIOピンの変更 : /gpio [pin-number]')
        continue
    if str.startswith('/LOG'):
        line = str.split()
        if len(line) == 2:
            if line[1] in on_list:
                log = True
                print(f"ログの表示は {log} に変更されました")
            elif line[1] in off_list:
                log = False
                print(f'ログの表示は {log} に変更されました')
            else:
                print('引数が不正です\nログの表示切り替え : /log [on / off]')
        else:
            print('引数が不正です\nログの表示切り替え : /log [on / off]')
        continue
    if str.startswith('/PINOUT'):
        line = str.split()
        if len(line) == 1:
             subprocess.run(['pinout'])
        continue
    if str.startswith('/EXIT'):
        break
    if str.startswith('/'):
        print('コマンドが見つかりません')
        continue

    # 文字ごとに処理
    for i in range(len(str)):
        if str[i] == " ": # スペースの場合
            if log :
                print("space")
            time.sleep(tick * 7)
            continue
        if str[i] == ".": # ピリオドの場合
            print("period")
            continue
        if (str[i] in alpha) == False: # アルファベットでない場合
            continue

        ch = morse[str[i]] # 辞書を引いてモールス信号を取得
        for j in range(len(ch)):
            if(ch[j] == "0"):
                ton()
            if(ch[j] == "1"):
                tu()
