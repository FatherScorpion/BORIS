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
safeAngle=0 #安全状態(モード0)の時に銃のロックが外れる角度
lockAngle=90 #射撃状態(モード1~2)の時に銃がロックされる角度
shotAngle=100 #引き金を引ける角度
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
  if mode==0: GPIO.output(ledPin[0], GPIO.HIGH) 
  else: GPIO.output(ledPin[0], GPIO.LOW) 
  if mode==1: GPIO.output(ledPin[1], GPIO.HIGH) 
  else: GPIO.output(ledPin[1], GPIO.LOW)
  if mode==2: GPIO.output(ledPin[2], GPIO.HIGH) 
  else: GPIO.output(ledPin[2], GPIO.LOW)
  if mode==3: GPIO.output(ledPin[3], GPIO.HIGH) 
  else: GPIO.output(ledPin[3], GPIO.LOW)

def checkSwitch():
  isOn=GPIO.input(swPin)
  if isOn:mode=mode+1
  if mode==4:mode=0
  time.sleep(0.5)

def checkGunlock():
  if mode==0:
   servoMotors[2].setAngle(safeAngle)
  else:servoMotors[2].setAngle(lockAngle)
 
def shot():
  servoMotors[2].setAngle(hoge)
  
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
