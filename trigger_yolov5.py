from datetime import datetime
import schedule
import time
import os
import detect

# path -> CCTV Video downloaded folder
# path = 'C:/Users/ngl/Desktop/Docker'
# path = "C:/Users/ngltr/OneDrive/Desktop/Docker"
print(" --- Find CCTV Video downloaded folder --- " )
print("Path_to_wacth_CCTV : ")
path = str(input())


def job():  # Run at 00:00
    dateformat = "%m%d%Y"
    past = folder_name = datetime.now().strftime(dateformat)  # 01012023
    if not os.path.isdir(path + "/" + folder_name):
        os.mkdir(path + "/" + folder_name)  # create folder on path
    path_to_watch = path + "/" + folder_name  # "C:/Users/ngltr/OneDrive/Desktop/Docker/12312022"
    old = os.listdir(path_to_watch)
    print("Ready to Run")
    while True:
        now = datetime.now().strftime(dateformat)
        if now != past:
            print("Date_Change : ", now)
            break
        new = os.listdir(path_to_watch)
        if len(new) > len(old):
            newfile = list(set(new) - set(old))
            print("New_File : ", newfile)
            for n in range(len(newfile)):
                print("Reading_File : ", newfile[n])
                old = new
                extension = os.path.splitext(path_to_watch + "/" + newfile[n])[1]
                if extension == ".mp4":
                    video_path = path_to_watch + "/" + str(newfile[n])
                    time.sleep(1)
                    read_cntr_number_region(video_path, folder_name)
                    # print("Video_Path : ", video_path)
                else:
                    continue
        else:
            continue


def read_cntr_number_region(video_path, folder_name):
    weight = "./runs/train/TruckNumber_yolov5s_results34/weights/best.pt"  # educated model
    video = video_path
    # video = "./Test_Video/video5.mp4"
    conf = 0.5
    detect.run(weights=weight, source=video, conf_thres=conf, name=folder_name)


# send_img_to_s3()
# time.sleep(10000)

# schedule.every().day.at("13:55").do(job) # Set schedule at 00:00 everyday
schedule.every(1).seconds.do(job)

while True:  # Run from here start scheduler
    schedule.run_pending()
