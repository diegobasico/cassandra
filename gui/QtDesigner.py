from os import startfile
from platform import node

qtdesigner_path = {
    'windows10': r"C:\Users\Diego\miniconda3\envs\cassandra\Library\lib\qt6\bin\designer.exe",
    'archlinux': r""
}

system_hostname = node()
startfile(qtdesigner_path[system_hostname])