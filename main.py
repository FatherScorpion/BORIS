from servo_motor import ServoMotor
import time
import RPi.GPIO as GPIO
import time
import sys
# ↑インポート

# ここからグローバル変数
nowX=0
nowY=0
mode=0 #0=停止,1=赤を打つ,2=黄色を打つ,3=人類は全員敵
swPin=23
ledPin=[4,17,7,22]
# ここまでグローバル変数

# ここから関数
def moveX(a):
  nowX=nowX+a
  if nowX>180:
    nowX=180
  elif nowX<0:
    nowX=0
  servoMotors[0].setAngle(nowX)

def moveY(a):
  nowY=nowY+a
  if nowY>90:
    nowY=90
  elif nowY<0:
      nowY=0
  servoMotors[1].setAngle(nowY)

def turnOnLedByMode():
  # ここを森君お願いします
  # モードによってLEDを切り替える処理です
  # modeというグローバル変数を用意したので、0~3までの範囲で切り替わる感じで
  # ピン番号はledPinという変数に持たせてあるので、気にしなくてよいです
  # ledPinは配列で、ledPin[0]~ledPin[3]のそれぞれをmode=0~3に対応させて下さい。
  # 必要があればグローバル変数はどんどん増やして大丈夫です
  # 以下に参考として、モード0用のLEDを点滅させるプログラムを書いておきます
  GPIO.output(ledPin[0], GPIO.HIGH) # ON
  GPIO.output(ledPin[0], GPIO.LOW) # OFF 0を他の数字に変えれば他のモードにも対応できます

def checkSwitch():
  isOn=GPIO.input(swPin)
  if isOn:mode=mode+1
  if mode==4:mode=0
  time.sleep(0.5)
  
# ここまで関数

# ここからセットアップ
GPIO.setmode(GPIO.BCM)
GPIO.setup(swPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
servoMotors = []

servoMotors.append(ServoMotor(Channel=0, ZeroOffset=0))
servoMotors.append(ServoMotor(Channel=1, ZeroOffset=0))
servoMotors.append(ServoMotor(Channel=2, ZeroOffset=0))

for i in range(180): # 起動した事を確認するためにモーターを適当に動かす
  moveX(1)
  moveY(1)
  time.sleep(0.01)
moveX(-180)
moveY(-180)
# ここまでセットアップ

# ここからループ処理
while 1:
  checkSwitch()
  turnOnLedByMode()
# ここまでループ処理