
# Pythono3 code to rename multiple
# files in a directory or folder

import os
def main():
    i = 0

    for filename in os.listdir("C:\\Users\\BAG\\Desktop\\CarCascade\\OwnCollection\\caryok\\non-car\\"):

        print(filename)
        dst = "images" + str(i) + ".png" #new name
        src = 'C:\\Users\\BAG\\Desktop\\CarCascade\\OwnCollection\\caryok\\non-car\\' + filename #add src path
        dst = 'C:\\Users\\BAG\\Desktop\\CarCascade\\OwnCollection\\caryok\\non-car\\' + dst #add dest path

        # rename() function will cars
        # rename all the files
        os.rename(src, dst)
        i += 1

if __name__ == '__main__':

    main()

