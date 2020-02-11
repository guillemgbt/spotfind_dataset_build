import os


def image_count(print_files=False):
    count = 0
    for root, dirs, files in os.walk("./Takes"):
        for file in files:
            if file.endswith(".jpg"):
                count+=1
                if print_files:
                    print(os.path.join(root, file))
    print(' --> '+str(count)+' drone images')


def main():
    image_count()


if __name__ == "__main__":
    main()
