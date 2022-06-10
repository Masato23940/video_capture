#!/usr/bin/env python
 
import sys
import time
import datetime

import cv2
import RPi.GPIO as GPIO
 
#/ dev/video0
DEV_ID = 0

# vcodeo param
WIDTH = 640
HEIGHT = 480
FPS = 30
SLEEP_TIME = 1/FPS;
RECODING_TIME_MAX = 10;
# ボタンは"GPIO5／GPIO6"に接続
BUTTON_A = 5
BUTTON_B = 6
 
# ボタンＡ／ボタンＢが押されたことを主処理に伝える
g_button_a = False
g_button_b = False
 
 
# 主処理
def main():
     
    # 関数内でグローバル変数を操作
    global g_button_a
    global g_button_b
     
    # 現在の状態を管理
    status = 0
     
    # 復帰中に経過時間を計測する
    resume = 0
     
    # 処理中に経過時間を計測する
    loop = 0
    # specify camera
    cap = cv2.VideoCapture(DEV_ID)

    # set parameter
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)
    cap.set(cv2.CAP_PROP_FPS, FPS)
    
    # file name
    date = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    path = "../Videos/Capture_Video/" + date + ".mp4"
    
    # video parameters for codec 
    fourcc = cv2.VideoWriter_fourcc('m','p','4','v')
    out = cv2.VideoWriter(path, fourcc, FPS, (WIDTH, HEIGHT))
    
    try:
        # 操作対象のピンは「GPIOn」の"n"を指定する
        GPIO.setmode(GPIO.BCM)
         
        # 使用するボタンの情報 [GPIOピン番号, コールバック関数]
        buttons = [
            [BUTTON_A, button_a_pressed],
            [BUTTON_B, button_b_pressed],
        ]
         
        for button in buttons:
            # ボタンがつながるGPIOピンの動作は「入力」「プルアップあり」
            GPIO.setup(button[0], GPIO.IN, pull_up_down=GPIO.PUD_UP)
             
            # 立ち下がり（GPIO.FALLING）を検出する（プルアップなので通常時1／押下時0）
            GPIO.add_event_detect(button[0], GPIO.FALLING, bouncetime=100)
            # イベント発生時のコールバック関数を登録
            GPIO.add_event_callback(button[0], button[1])
         
        # 無限ループ
        while True:
            # 30ミリ秒間休止(30FPS)
            time.sleep(SLEEP_TIME)
             
            # 「待機中」はボタンＡを確認して処理を起動する
            if status == 0:
                if g_button_a:
                    # 状態を「処理中」に
                    status = 1
                    print_message("button A was pressed. start recording")
             
            # 「処理中」はボタンＢを確認して処理をキャンセル
            elif status == 1:
                loop += 1
                
                # capture
                ret, frame = cap.read()
                out.write(frame)
    
                if g_button_b:
                    # キャンセル。状態を「復帰中」に
                    status = 2
                    loop = 0
                    print_message("button B was pressed. stop recording")
                elif FPS*RECODING_TIME_MAX < loop:
                    # 終了。状態を「復帰中」に
                    status = 2
                    loop = 0
                    print_message("recording stopped")
                elif loop % (FPS*2) == 0:
                    # 2秒おきにメッセージ
                    print_message("recording...")
             
            # 「復帰中」は1秒経過するのを待つ
            elif status == 2:
                # ループの回数をカウント
                resume += 1
                #release
                cap.release()
                out.release()
                cv2.destroyAllWindows()
                
                if 10 <= resume:
                    # 1秒経過したので状態を「待機中」に
                    status = 0
                    resume = 0
                    print_message("1秒経過しました。待機中に遷移")
             
            # ボタンが押されたことは上のif文で確認済み
            g_button_a = False
            g_button_b = False
     
    # キーボード割り込みを捕捉
    except KeyboardInterrupt:
        print("例外'KeyboardInterrupt'を捕捉")
     
    print("処理を終了します")
     
    # GPIOの設定をリセット
    GPIO.cleanup()
     
    return 0
 
 
# ボタンＡが押された時に呼び出されるコールバック関数
# gpio_no: イベントの原因となったGPIOピンの番号
def button_a_pressed(gpio_no):
     
    # 関数内でグローバル変数を操作
    global g_button_a
    g_button_a = True
 
 
# ボタンＢが押された時に呼び出されるコールバック関数
# gpio_no: イベントの原因となったGPIOピンの番号
def button_b_pressed(gpio_no):
     
    # 関数内でグローバル変数を操作
    global g_button_b
    g_button_b = True
 
 
# ターミナル上に「日付 時刻.マイクロ秒: メッセージ」を表示する関数
# message: 表示する「メッセージ」
def print_message(message):
     
    # 現在の日付時刻を取得して「年-月-日 時:分:秒.マイクロ秒」にフォーマット
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S.%f")
     
    # 引数で送られたメッセージを表示
    print("{}: {}".format(timestamp, message))
 
 
if __name__ == "__main__":
    sys.exit(main())
