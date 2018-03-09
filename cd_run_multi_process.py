import sys, os,subprocess, threading
import re
import time
from multiprocessing import Process, Pool, cpu_count

        
def run_func(directory_list):
##    print(f'Run child process {os.getpid()}')
    for directory in directory_list:
        cd_directory = re.sub(r'/orders.http_api.json','',directory)
        print(cd_directory)
        os.chdir(cd_directory)
        #subprocess.call(['touch', 'new7.txt'])
        with open('QA.ini', 'w') as f:
            f.write('[run]\n\n')
            f.write('[diff]\n')
        

if __name__ == '__main__':

    start_time = time.time()
    current_directory = os.getcwd()

    contents = subprocess.check_output(["find", current_directory, "-name", "orders.http_api.json"],universal_newlines=True)
    L = contents.split('\n')
    ##print(L)
    R = [i for i in L if i]
    R.sort()
    print(len(R))

    r = len(R) // cpu_count() + 1
    n = r
    
    index0 = 0
    task_list = []
    for i in range(cpu_count()):
        task_list.append(R[index0: n])
        index0 = n
        n = n + r


    



##    for i in task_list:
##        print('***')
##        print(i[0])
##        print(i[1])



    p = Pool(cpu_count())
    for directory in task_list:
        p.apply_async(run_func, args=(directory, ))
        
    p.close()
    p.join()
    
 



    ##multi thread

    #sys.exit()
    
##    for directory in task_list:
##        t = threading.Thread(target = run_func, args=(directory, ))
##        t.setDaemon(True)
##        t.start()
##    t.join()

    end_time = time.time()
    print(f'total time: {end_time - start_time}')
    
    

    
    
