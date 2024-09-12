# import os
# import subprocess
# from platform import node

# qtdesigner_path = {
#     'windows10': r"C:\Users\Diego\miniconda3\envs\cassandra\Library\lib\qt6\bin\designer.exe",
#     'archlinux': r"/home/diego/miniconda3/envs/cassandra/lib/qt6/bin/designer"
# }

# path = {
#     'windows10': r"os.startfile(C:\Users\Diego\miniconda3\envs\cassandra\Library\lib\qt6\bin\designer.exe)",
#     'archlinux': r"subprocess.run(/home/diego/miniconda3/envs/cassandra/lib/qt6/bin/designer)"
# }

# system_hostname = node()
# exec(path[system_hostname])

import os
import subprocess
import platform


qtdesigner_path = {
    'Windows': r"C:\Users\Diego\miniconda3\envs\cassandra\Library\lib\qt6\bin\designer.exe",
    'Linux': r"/home/diego/miniconda3/envs/cassandra/lib/qt6/bin/designer"
}
system = platform.system()

def main():
    if system == 'Windows':
        os.startfile(qtdesigner_path['Windows'])  # For Windows
    elif system == 'Linux':
        subprocess.run([qtdesigner_path['Linux']])  # For Linux
    else:
        print(f"Operating system '{system}' is not supported.")

if __name__ == '__main__':
    main()