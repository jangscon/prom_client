import os

def file_count(filepath):
    return len(os.listdir(filepath))

def read_latency(filepath):
    pass

if __name__ == "__main__":
    print(file_count("/home/dom/dom/images"))
    