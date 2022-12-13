from servo_motor import ServoMotor
import time

nowX=0
nowY=0

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

servoMotors = []

servoMotors.append(ServoMotor(Channel=0, ZeroOffset=0))
servoMotors.append(ServoMotor(Channel=1, ZeroOffset=0))
servoMotors.append(ServoMotor(Channel=2, ZeroOffset=0))

for i in range(180):
  servoMotors[0].setAngle(i)
  servoMotors[1].setAngle(i)
  servoMotors[2].setAngle(i)
  print(i)
  time.sleep(0.01)
servoMotors[0].setAngle(0)
servoMotors[1].setAngle(0)
servoMotors[2].setAngle(0)

for i in range(180):
  moveX(1)
  moveY(1)
  time.sleep(0.01)
moveX(-180)
moveY(-180)
