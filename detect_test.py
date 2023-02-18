import detect_pose
import time

def main():
    detect_pose.initialize()

    while(1):
        hoge = input("next:")
        if hoge == "exit": break

        time.sleep(5)
        detect_pose.getPoseFromCamera()
    
    detect_pose.disable()
    return

if __name__ == "__main__":
    main()
