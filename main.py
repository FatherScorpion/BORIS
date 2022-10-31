from servo_motor import ServoMotor
import time

nowX=0
nowY=0

def moveX(a): #X方向(横向き)にa度動かす
  # ここを追記・修正
  servoMotors[0].setAngle(a)

def moveY(a): #Y方向(縦向き)にa度動かす
  # ここを追記・修正
  servoMotors[1].setAngle(a)

servoMotors = []

servoMotors.append(ServoMotor(Channel=0, ZeroOffset=0))
servoMotors.append(ServoMotor(Channel=1, ZeroOffset=0))
servoMotors.append(ServoMotor(Channel=3, ZeroOffset=0))

for i in range(5):
  servoMotors[0].setAngle(nowX)
  servoMotors[1].setAngle(nowY)
  servoMotors[2].setAngle(i*90)
  nowX+=90
  nowY+=90
  time.sleep(1)
servoMotors[0].setAngle(0)
servoMotors[1].setAngle(0)
servoMotors[2].setAngle(0)
nowX=0
nowY=0

for i in range(4):
  moveX(90)
  moveY(90)
  time.sleep(1)
moveX(-360)
moveY(-360)