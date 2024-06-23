from datetime import datetime
import schedule
import time
import os
import detect  # Assuming detect is a custom module you've implemented

# Function to perform the job
def job():
    dateformat = "%m%d%Y"
    current_date = datetime.now().strftime(dateformat)  # Current date in format 01012023
    folder_path = os.path.join(path, current_date)
    
    # Create folder if it doesn't exist
    if not os.path.isdir(folder_path):
        os.mkdir(folder_path)
    
    print("Ready to Run - YOLO_Engine")
    
    # Watch for changes in the specified folder
    while True:
        now = datetime.now().strftime(dateformat)
        
        # Check if date has changed to break out of the loop
        if now != current_date:
            print("Date changed: ", now)
            break
        
        # Retrieve list of files in the folder
        current_files = os.listdir(folder_path)
        
        # Detect new files added since last check
        if len(current_files) > len(previous_files):
            new_files = list(set(current_files) - set(previous_files))
            print("New File(s): ", new_files)
            
            # Process each new video file
            for new_file in new_files:
                print("Processing File: ", new_file)
                file_extension = os.path.splitext(new_file)[1]
                
                # Check if the file is a video (.mp4)
                if file_extension == ".mp4":
                    video_path = os.path.join(folder_path, new_file)
                    time.sleep(1)  # Optional delay before processing
                    
                    # Call your function to process the video
                    read_cntr_number_region(video_path, current_date)
                else:
                    continue
        
        # Update the list of files for the next iteration
        previous_files = current_files
        time.sleep(1)  # Adjust sleep time as needed


def read_cntr_number_region(video_path, folder_name):
    # Example weights and configuration
    weight = "./runs/train/TruckNumber_yolov5s_results34/weights/best.pt"
    conf_threshold = 0.5
    
    # Run detection using your custom detect module
    detect.run(weights=weight, source=video_path, conf_thres=conf_threshold, name=folder_name)
    print("Detection Completed at: ", datetime.now())


# Main script starts here

# Define the path where the CCTV videos will be downloaded
print("\nC:\\Users\\frank\\OneDrive\\Desktop\\Docker")
print("--- Find CCTV Video downloaded folder ---")
print("Path to watch CCTV: ")
path = input().strip()  # Get path from user input

# Set up the schedule to run the job periodically (every 1 second in this case)
schedule.every(1).seconds.do(job)

# Main loop to run the scheduler
while True:
    schedule.run_pending()
    time.sleep(1)  # Adjust sleep time to control scheduler frequency