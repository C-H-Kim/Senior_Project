import os
import shutil
from PIL import Image

def create_dir_if_not_exist(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

size = 224
qual = 75

if os.path.exists(f"./resize_{size}_{qual}/"):
    try:
        shutil.rmtree(f"./resize_{size}_{qual}/")
        print(f"Directory \"resize_{size}_{qual}\" does exist already. Removing complete")
        print()
    except:
        print(f"Directory \"resize_{size}_{qual}\" does not exist.")
        print()
        pass

main_path = "/home/chkim/after_remove_dissimilar/"
os.chdir(main_path)

for i in os.listdir(os.getcwd()):
    save_path = f"/home/chkim/resize_{size}_{qual}/{i}/"
    create_dir_if_not_exist(save_path)
    print(f"Directory \"resize_{size}_{qual}/{i}\" create complete")

    os.chdir(main_path + i)
    for file in os.listdir(os.getcwd()):
        img = Image.open(file)
        if img.mode != 'RGB':
            img = img.convert('RGB')
        img_resize = img.resize((size, size))
        img_resize.save(save_path + f"{file}")

    print(f"{i:<25}| resize complete.")
    print()

print("Done.")
