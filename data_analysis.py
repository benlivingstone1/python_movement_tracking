import pandas as pd

def time_spent(counts):
    # to figure out, use command: ffprobe -v error -select_streams v:0 -show_entries stream=r_frame_rate -of default=noprint_wrappers=1:nokey=1 <path/to/your/video/file.mp4>
    frame_rate = 30
    time = counts / frame_rate
    return time

if __name__ == "__main__":
    df = pd.read_csv("centroid.csv")
    
    locations = {0: "triangle",
                 1: "square",
                 2: "connector"}
    
    df["location"] = df["location"].map(locations)
    
    counts_location = df["location"].value_counts()
    triangle_counts = counts_location["triangle"]
    square_counts = counts_location["square"]
    connector_counts = counts_location["connector"]

    triangle_time = time_spent(triangle_counts)
    square_time = time_spent(square_counts)
    connector_time = time_spent(connector_counts)

    print(f"seconds in triangle: {triangle_time}\n", 
          f"seconds in square: {square_time}\n", 
          f"seconds in connector: {connector_time}")

