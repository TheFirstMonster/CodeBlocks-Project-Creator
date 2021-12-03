import os
import subprocess
import shutil

PREFIX = ""
TEMPLATE_FILE = "template.cbp"
PROJECT_DIR = "../CodeBlocks/"
CODEBLOCKS_CMD = r'"C:\Program Files\CodeBlocks\codeblocks.exe" {} /na /nd /ns --multiple-instance'

def main():
    
    while True:
        source_dir = input("Folder to copy: ")
        if not os.path.isdir(source_dir):
            print("Invalid path: Directory doesn't exist.")
        else:
            break
            
    project_name = input("Project name: ")
    
    dirname = PROJECT_DIR + project_name
    
    if os.path.exists(dirname):
        print("ERROR: This directory already exists.")
        return
    else:
        os.mkdir(dirname)
    
    filename = PROJECT_DIR + project_name + "/" + project_name + ".cbp"
    
    with open(TEMPLATE_FILE, "r") as f:
        contents = f.readlines()

    for file in os.listdir(source_dir):
        if file.endswith((".cpp", ".c", ".hpp", ".h")):
            print("Found source file {}".format(file))
            shutil.copy(os.path.join(source_dir, file), dirname)
            contents.insert(34, '\t\t<Unit filename="{}" />\n'.format(file))
        
    if not os.listdir(dirname):
        print("ERROR: No source files found.")
        return
    
    contents = "".join(contents)
    contents = contents.replace("$NAME$", project_name)

    with open(filename, "w+") as f:
        f.writelines(contents)
    
    os.system(CODEBLOCKS_CMD.format(filename) + " --build")
    
    shutil.make_archive(dirname + "/" + PREFIX + " " + project_name, "zip", dirname)
    
    print("Successfully created project at " + filename)
    
    x = input("Open in CodeBlocks (y/n): ")
    if x.lower() == "y":
        subprocess.Popen(CODEBLOCKS_CMD.format(filename))
    
    
if __name__ == "__main__":
    main()
    input("Press any key to exit...")
    