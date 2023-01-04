from datetime import datetime
import schedule
import time
import os
import detect

path = "C:/Users/ngltr/OneDrive/Desktop/Docker"


def job():  # Run at 00:00
    now = datetime.now()
    folder_name = str(now.strftime("%m")) + str(now.strftime("%d")) + str(now.strftime("%Y"))  # 20230101
    if not os.path.isdir(path + "/" + folder_name):
        os.mkdir(path + "/" + folder_name)  # create folder on path
    path_to_watch = path + "/" + folder_name  # "C:/Users/ngltr/OneDrive/Desktop/Docker/12312022"
    old = os.listdir(path_to_watch)
    print("Ready to Run")
    while True:
        new = os.listdir(path_to_watch)
        if len(new) > len(old):
            newfile = list(set(new) - set(old))
            print("New_File : ", newfile[0])
            old = new
            extension = os.path.splitext(path_to_watch + "/" + newfile[0])[1]
            if extension == ".mp4":
                video_path = path_to_watch + "/" + str(newfile[0])
                read_cntr_number_region(video_path)
                # print("Video_Path : ", video_path)
                print("폴더 확인 : ", newfile)
            else:
                continue
        else:
            continue


def read_cntr_number_region(video_path):
    weight = "./runs/train/TruckNumber_yolov5s_results34/weights/best.pt" # educated model
    video = video_path
    # video = "./Test_Video/video5.mp4"
    conf = 0.5
    detect.run(weights=weight, source=video, conf_thres=conf)


# schedule.every().day.at("13:55").do(job) # Set schedule at 00:00 everyday
schedule.every(1).seconds.do(job)

while True:  # Run from here start scheduler
    schedule.run_pending()
