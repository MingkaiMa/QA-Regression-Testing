import sys, subprocess, os
import re
from multiprocessing import Process, Pool, cpu_count
import configparser


def run_func(directory_list):
    print(f'Run {os.getpid()}')



    for directory in directory_list:
        cd_directory = re.sub(r'/orders.http_api.json', '', directory)
        os.chdir(cd_directory)
        dir_list = cd_directory.split('/')

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
#        print(dic)
#        for i in dic:
#            print(i, '---', dic[i])


        mode = dic['run']['mode']
        args = dic['run']['args']
        pargs = dic['run']['pargs']
        
        cmd1 = pargs + ' ' + '/opt/shared/heptax/bin/vspy.run' + ' ' + args
        cmd2 = pargs + ' ' + '/opt/shared/heptax/bin/vspc.run' + ' ' + args
        


        if mode == 'py':
            subprocess.call(cmd1, shell=True)
        elif mode == 'cpp':
            subprocess.call(cmd2, shell=True)
        elif mode == 'pycxx':
            subprocess.call(cmd1, shell=True)
            subprocess.call(cmd2, shell=True)
        


def copy_py_au(directory_list, cmd3):
    print(f'Run {os.getpid()}')
    for directory in directory_list:
        cd_directory = re.sub(r'/orders.http_api.json', '', directory)
        os.chdir(cd_directory)
        subprocess.call(cmd3, shell=True)

current_directory = os.getcwd()

cmd1 = '/opt/shared/heptax/bin/vspy.run'
cmd2 = '/opt/shared/heptax/bin/vspc.run'
cmd3 = 'cp output_plans.json  output_plans.au.json'

contents = subprocess.check_output(["find", current_directory, "-name", "orders.http_api.json"],universal_newlines=True)
L = contents.split('\n')
R = [i for i in L if i]
R.sort()
print(len(R))
print(R[0])

r = len(R) // cpu_count() + 1
n = r

index0 = 0
task_list = []
for i in range(cpu_count()):
    task_list.append(R[index0: n])
    index0 = n
    n = n + r

print(len(task_list))
##
##for i in task_list:
##    print(i)
##    print('**', len(i))


p = Pool(cpu_count())
#for directory in task_list:
    #p.apply_async(copy_py_au, args=(directory, cmd3))
    #p.apply_async(run_func, args=(directory))

p.map(run_func, task_list)
    
p.close()
p.join()




