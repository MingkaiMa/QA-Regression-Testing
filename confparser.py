import configparser
import sys, os,subprocess, threading
import re
import time
from multiprocessing import Process, Pool, cpu_count

config = configparser.ConfigParser()


def run_func(directory_list):
##    print(f'Run child process {os.getpid()}')
##    for directory in directory_list:
    directory = directory_list
    print(directory, '___')

    cd_directory = re.sub(r'/orders.http_api.json','',directory)
    os.chdir(cd_directory)
    print(cd_directory)
    dir_list = cd_directory.split('/')
    print(dir_list)
    print('/'.join(dir_list))
##    print(os.path.join('1', '2'))
    config4 = '/'.join(dir_list) + '/QA.ini'
    config3 = '/'.join(dir_list[:-1]) + '/QA.ini'
    config2 = '/'.join(dir_list[:-2]) + '/QA.ini'
    config1 = '/'.join(dir_list[:-3]) + '/QA.ini'
    print(config1)
    print(config2)
    print(config3)
    print(config4)
    config_list = []
    config_list.append(config1)
    config_list.append(config2)
    config_list.append(config3)
    config_list.append(config4)
    config = configparser.ConfigParser()
    for con in config_list:
        config.read(con)

    
    dic = config._sections
    print(dic)
    for i in dic:
        print(i, '---', dic[i])

    print(dic['run']['mode'] == 'py')

    return 
    

    #subprocess.call(['touch', 'new7.txt'])
    with open('QA.ini', 'w') as f:
        f.write('[run]\n\n')
        f.write('[diff]\n')
        



current_directory = os.getcwd()
contents = subprocess.check_output(["find", current_directory, "-name", "orders.http_api.json"],universal_newlines=True)
L = contents.split('\n')
R = [i for i in L if i]
R.sort()


for i in R:
    print(i)
    run_func(i)
    sys.exit()

##r = len(R) // cpu_count() + 1
##n = r
##
##index0 = 0
##task_list = []
##for i in range(cpu_count()):
##    task_list.append(R[index0: n])
##    index0 = n
##    n = n + r
##
##
##
##p = Pool(cpu_count())
##for directory in task_list:
##    p.apply_async(run_func, args=(directory, ))
##    
##p.close()
##p.join()
    
