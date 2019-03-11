import os
import zipfile

# 解压
with zipfile.ZipFile(r'C:\Users\DF\Desktop\nas\vm-all-1.csar', 'r') as mano_csar:
    mano_csar.extractall(r'C:\Users\DF\Desktop\nas')

# 压缩文件
with zipfile.ZipFile(r'C:\Users\DF\Desktop\spring_mvc.zip', 'w', zipfile.ZIP_DEFLATED) as to_zip_file:
    to_zip_file.write(r'C:\Users\DF\Desktop\corejava9')


# 压缩文件夹
def zip_folder(folder_path, output_path):
    """Zip the contents of an entire folder (with that folder included
    in the archive). Empty subfolders will be included in the archive
    as well.
    """
    parent_folder = os.path.dirname(folder_path)
    # Retrieve the paths of the folder contents.
    contents = os.walk(folder_path)
    try:
        zip_file = zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED)
        for root, folders, files in contents:
            # Include all subfolders, including empty ones.
            for folder_name in folders:
                absolute_path = os.path.join(root, folder_name)
                relative_path = absolute_path.replace(parent_folder + '\\', '')
                print("Adding '%s' to archive." % absolute_path)
                zip_file.write(absolute_path, relative_path)
            for file_name in files:
                absolute_path = os.path.join(root, file_name)
                relative_path = absolute_path.replace(parent_folder + '\\', '')
                print("Adding '%s' to archive." % absolute_path)
                zip_file.write(absolute_path, relative_path)
        print("'%s' created successfully." % output_path)
    except Exception as e:
        print(e)
    finally:
        zip_file.close()


# TEST
if __name__ == '__main__':
    zip_folder(r'D:\[STORAGE]\Software\TrueCrypt', r'D:\[STORAGE]\Software\TrueCrypt.zip')
