from servo_motor import ServoMotor
import time
import RPi.GPIO as GPIO
import time
import sys
# ↑インポート

# ここからグローバル変数
nowX=0
nowY=0
minX=0
minY=0
maxX=180
maxY=90
defX=90
defY=0

mode=0 #0=停止,1=赤を打つ,2=黄色を打つ,3=人類は全員敵
swPin=23
ledPin=[4,17,7,22]
safeAngle=0 #安全状態(モード0)の時に銃のロックが外れる角度
lockAngle=90 #射撃状態(モード1~2)の時に銃がロックされる角度
shotAngle=100 #引き金を引ける角度
# ここまでグローバル変数

# ここから関数
def moveX(a):
  global nowX
  global maxX
  global minX
  nowX=nowX+a
  if nowX>maxX:
    nowX=maxX
  elif nowX<minX:
    nowX=minX
  servoMotors[0].setAngle(nowX)

def moveY(a):
  global nowY
  global maxY
  global minY
  nowY=nowY+a
  if nowY>maxY:
    nowY=maxY
  elif nowY<minY:
      nowY=minY
  servoMotors[1].setAngle(nowY)

def turnOnLedByMode():
  global mode
  if mode==0: GPIO.output(ledPin[0], GPIO.HIGH) 
  else: GPIO.output(ledPin[0], GPIO.LOW) 
  if mode==1: GPIO.output(ledPin[1], GPIO.HIGH) 
  else: GPIO.output(ledPin[1], GPIO.LOW)
  if mode==2: GPIO.output(ledPin[2], GPIO.HIGH) 
  else: GPIO.output(ledPin[2], GPIO.LOW)
  if mode==3: GPIO.output(ledPin[3], GPIO.HIGH) 
  else: GPIO.output(ledPin[3], GPIO.LOW)

def checkSwitch():
  global swPin
  global mode
  isOn=GPIO.input(swPin)
  if isOn:
    mode=mode+1
    time.sleep(0.5)
  if mode==4:mode=0

def checkGunlock():
  global mode
  global safeAngle
  global lockAngle
  if mode==0:
   servoMotors[2].setAngle(safeAngle)
  else:servoMotors[2].setAngle(lockAngle)

def shot():
  global shotAngle
  global lockAngle
  servoMotors[2].setAngle(shotAngle)
  time.sleep(0.5)
  servoMotors[2].setAngle(lockAngle)
# ここまで関数

# ここからセットアップ
GPIO.setmode(GPIO.BCM)
GPIO.setup(swPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(ledPin[0], GPIO.OUT)
GPIO.setup(ledPin[1], GPIO.OUT)
GPIO.setup(ledPin[2], GPIO.OUT)
GPIO.setup(ledPin[3], GPIO.OUT)
servoMotors = []

servoMotors.append(ServoMotor(Channel=0, ZeroOffset=0))
servoMotors.append(ServoMotor(Channel=1, ZeroOffset=0))
servoMotors.append(ServoMotor(Channel=2, ZeroOffset=0))

# ここまでセットアップ

# ここからループ処理
while 1:
  checkSwitch()
  turnOnLedByMode()
  checkGunlock()
  if mode==0:
    servoMotors[0].setAngle(defX)
    servoMotors[1].setAngle(defY)
    nowX=defX
    nowY=defY
  if mode==1:
    servoMotors[0].setAngle(maxX)
    servoMotors[1].setAngle(maxY)
    nowX=maxX
    nowY=maxY
  if mode==2:
    servoMotors[0].setAngle(minX)
    servoMotors[1].setAngle(minY)
    nowX=minX
    nowY=minY
  if mode==3:
    shot()
# ここまでループ処理
