from deepdiff import DeepDiff
from pprint import pprint
from datetime import datetime
import json
import sys, subprocess, os
import re
import time
from multiprocessing import Process, Pool, cpu_count, Manager
import configparser



relative_small = 0.001

def compare(filename_11, filename_22, case, log_file, relative_tole, abs_tole, case_sensitive):
    with open(filename_11) as json_file:
        json_data = json.load(json_file)

    with open(filename_22) as json_file_2:
        json_data2 = json.load(json_file_2)

    a = dict(DeepDiff(json_data, json_data2))


    filename_1 = filename_11.split('/')[-1]
    filename_2 = filename_22.split('/')[-1]

    with open(log_file, 'a') as f:
        f.write(f'\n{datetime.now()}\n')
        f.write(f'compare {filename_1} and {filename_2}\n\n')

    if not a:
        return 0

        
    same_flag = True
    all_add_dic = {}
    all_changed_dic_1 = {}
    all_changed_dic_2 = {}
    all_remove_dic = {}

    
    for key in a:
        
        if 'changed' in key:
            
            changed_dic = a[key]
            for changed_key in changed_dic:
                changed_1_key_dic = re.sub(r'root', 'json_data', changed_key)
                changed_2_key_dic = re.sub(r'root', 'json_data2', changed_key)

                if type(eval(changed_1_key_dic)) == type('str') and type(eval(changed_2_key_dic)) == type('str'):
                    
                    if case_sensitive == '1':
                        if eval(changed_1_key_dic) != eval(changed_2_key_dic):
                            same_flag = False
                            with open(log_file, 'a') as f:
                                f.write(f'{changed_key}: ')
                                l = len(changed_key)
                                f.write(' ' * l, end='')
                                f.write(f'{filename_1} value: {eval(changed_1_key_dic)}')
                                f.write(' ' * l, end='')
                                f.write(f'{filename_2} value: {eval(changed_2_key_dic)}')

                    elif case_sensitive == '0':
                        if eval(changed_1_key_dic).lower() != eval(changed_2_key_dic).lower():
                            same_flag = False
                            with open(log_file, 'a') as f:
                                f.write(f'{changed_key}: ')
                                l = len(changed_key)
                                f.write(' ' * l, end='')
                                f.write(f'{filename_1} value: {eval(changed_1_key_dic)}')
                                f.write(' ' * l, end='')
                                f.write(f'{filename_2} value: {eval(changed_2_key_dic)}')

                elif eval(str(eval(changed_1_key_dic))) <= abs_tole and eval(str(eval(changed_2_key_dic))) <= abs_tole:
                    pass

                elif abs(eval(str(eval(changed_1_key_dic))) - eval(str(eval(changed_2_key_dic)))) > relative_tole:

                    same_flag = False
                    with open(log_file, 'a') as file:
                        file.write(f'{changed_key}: \n')
                        l = len(changed_key)
                        file.write(' ' * l)
                        file.write(f'{filename_1} value: {eval(changed_1_key_dic)}\n')
                        file.write(' ' * l)
                        file.write(f'{filename_2} value: {eval(changed_2_key_dic)}\n\n')


        if 'type_changes' in key:
            type_changed_dic = a[key]
            for type_key in type_changed_dic:
                changed_1_key_dic = re.sub(r'root', 'json_data', type_key)
                changed_2_key_dic = re.sub(r'root', 'json_data2', type_key)


                if (type(eval(changed_1_key_dic)) == type(True) or type(eval(changed_2_key_dic)) == type(True)):

                    if eval(changed_1_key_dic) != eval(changed_2_key_dic):
                        same_flag = False
                        with open(log_file, 'a') as f:
                            f.write(f'{type_key}: \n')
                            l = len(type_key)
                            f.write(' ' * l)
                            f.write(f'{filename_1} value: {eval(changed_1_key_dic)}\n')
                            f.write(' ' * l)
                            f.write(f'{filename_2} value: {eval(changed_2_key_dic)}\n\n')
                        continue



                if abs(eval(str(eval(changed_1_key_dic))) - eval(str(eval(changed_2_key_dic)))) > relative_tole:
                    same_flag = False
                    with open(log_file, 'a') as f:
                        f.write(f'{type_key}: \n')
                        l = len(type_key)
                        f.write(' ' * l)
                        f.write(f'{filename_1} value: {eval(changed_1_key_dic)}\n')
                        f.write(' ' * l)
                        f.write(f'{filename_2} value: {eval(changed_2_key_dic)}\n\n')


        if 'removed' in key:
            same_flag = False
            removed_dic = a[key]
            for removed_key in removed_dic:
                removed_key_dic = re.sub(r'root', 'json_data', removed_key)
                all_remove_dic[removed_key] = eval(removed_key_dic)


        if 'added' in key:
            same_flag = False
            added_dic = a[key]
            for added_key in added_dic:
                added_key_dic = re.sub(r'root','json_data2', added_key)

                all_add_dic[added_key] = eval(added_key_dic)



    for key in all_remove_dic:


        with open(log_file, 'a') as f:
            f.write(f'{key}: \n')
            l = len(key)
            f.write(' ' * l)
            f.write(f'{filename_1} value: {all_remove_dic[key]}\n')
            f.write(' ' * l)
            f.write(f'{filename_2} value: not exist\n\n')
                

    for key in all_add_dic:


        with open(log_file, 'a') as f:
            f.write(f'{key}: \n')
            l = len(key)
            f.write(' ' * l)
            f.write(f'{filename_1} value: not exist\n')
            f.write(' ' * l)
            f.write(f'{filename_2} value: {all_add_dic[key]}\n\n')



    if same_flag == False:
        return 1
    else:
        return 0


current_directory = os.getcwd()
summary_file = os.path.join(current_directory, 'summary.txt')

##options:
## pc: compare python and cxx
## pa: compare python and au
## ca: compare cxx and au
## all: compare all

##option = 'all'
##if len(sys.argv) == 2:
##    option = sys.argv[1]
##
##print(option)



contents = subprocess.check_output(["find", current_directory, "-name", "orders.http_api.json"],universal_newlines=True)
L = contents.split('\n')
##print(L)
R = [i for i in L if i]
R.sort()
##print(R)
print(len(R))



def run_func(directory_list, summary_file, failed_list, passed_list):


    for directory in directory_list:

        
        file_miss_flag = False
        fail_flag = False

        cd_directory = re.sub(r'/orders.http_api.json','',directory)
        os.chdir(cd_directory)

        dir_list = cd_directory.split('/')
        #print(dir_list)
        #print('/'.join(dir_list))
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
        #print(dic)
        #for i in dic:
         #   print(i, '---', dic[i])

        option = dic['diff']['mode']
        relative_tole = float(dic['diff']['relative_tole'])
        abs_tole = float(dic['diff']['abs_tole'])
        case_sensitive = dic['diff']['case_sensitive']
                
        log_file = 'test_log.txt'

        file_au = os.path.join(cd_directory, 'output_plans.au.json')
        file_py = os.path.join(cd_directory, 'output_plans.json')
        file_cxx = os.path.join(cd_directory, 'cxx_outplans.json')


        if option == 'all':
            if not os.path.isfile(file_py):
                file_miss_flag = True
                with open('test_log.txt', 'a') as file:
                    file.write(f'\n{datetime.now()}\n')
                    file.write('output_plans.json missed\n')

            if not os.path.isfile(file_cxx):
                file_miss_flag = True
                with open('test_log.txt', 'a') as file:
                    file.write(f'\n{datetime.now()}\n')
                    file.write('cxx_outplans.json missed\n')

            if file_miss_flag == True:
                failed_list.append(cd_directory)
                #failed_test += 1
                with open(summary_file, 'a') as sumf:
                    sumf.write(f'case: {cd_directory} ----failed\n\n')
                    sumf.write(f'miss file\n')
                    sumf.write('\n')
                    
                continue

            result_au_py = compare(file_au, file_py, cd_directory, log_file, relative_tole, abs_tole, case_sensitive)
            result_au_cxx = compare(file_au, file_cxx, cd_directory, log_file, relative_tole, abs_tole, case_sensitive)
            result_py_cxx = compare(file_py, file_cxx, cd_directory, log_file, relative_tole, abs_tole, case_sensitive)

            case_fail_flag = False
            
            if result_au_py == 1 or result_au_cxx == 1 or result_py_cxx == 1:
                case_fail_flag = True

            if case_fail_flag == True:
                failed_list.append(cd_directory)
                #failed_test += 1
                with open(summary_file, 'a') as f:
                    f.write(f'case: {cd_directory} ----failed\n\n')
                    f.write(f'test failed\n')
                    f.write('\n')

                if result_au_py == 1:
                    with open(summary_file, 'a') as f:
                        f.write('output_plans.au.json -- output_plans.json  failed\n\n')

                if result_au_cxx == 1:
                    with open(summary_file, 'a') as f:
                        f.write('output_plans.au.json -- cxx_outplans.json   failed\n\n')

                if result_py_cxx == 1:
                    with open(summary_file, 'a') as f:
                        f.write('output_plans.json -- cxx_outplans.json   failed\n\n')

            elif case_fail_flag == False:
                passed_list.append(cd_directory)
                #successed_test += 1
                with open(summary_file, 'a') as f:
                    f.write(f'case: {cd_directory} ----passed\n\n')

        elif option == 'pc':
            
            if not os.path.isfile(file_py):
                file_miss_flag = True
                with open('test_log.txt', 'a') as file:
                    file.write(f'\n{datetime.now()}\n')
                    file.write('output_plans.json missed\n')

            if not os.path.isfile(file_cxx):
                file_miss_flag = True
                with open('test_log.txt', 'a') as file:
                    file.write(f'\n{datetime.now()}\n')
                    file.write('cxx_outplans.json missed\n')

            if file_miss_flag == True:
                failed_list.append(cd_directory)
                #failed_test += 1
                with open(summary_file, 'a') as sumf:
                    sumf.write(f'case: {cd_directory} ----failed\n\n')
                    sumf.write(f'miss file\n')
                    sumf.write('\n')
                    
                continue

            #result_au_py = compare(file_au, file_py, cd_directory, log_file)
            #result_au_cxx = compare(file_au, file_cxx, cd_directory, log_file)
            result_py_cxx = compare(file_py, file_cxx, cd_directory, log_file, relative_tole, abs_tole, case_sensitive)

            case_fail_flag = False
            
            if result_py_cxx == 1:
                case_fail_flag = True

            if case_fail_flag == True:
                failed_list.append(cd_directory)
                #failed_test += 1
                with open(summary_file, 'a') as f:
                    f.write(f'case: {cd_directory} ----failed\n\n')
                    f.write(f'test failed\n')
                    f.write('\n')

                if result_py_cxx == 1:
                    with open(summary_file, 'a') as f:
                        f.write('output_plans.json -- cxx_outplans.json   failed\n\n')

            elif case_fail_flag == False:
                passed_list.append(cd_directory)
                #successed_test += 1
                with open(summary_file, 'a') as f:
                    f.write(f'case: {cd_directory} ----passed\n\n')

        elif option == 'pa':
            if not os.path.isfile(file_py):
                file_miss_flag = True
                with open('test_log.txt', 'a') as file:
                    file.write(f'\n{datetime.now()}\n')
                    file.write('output_plans.json missed\n')

    ##        if not os.path.isfile(file_cxx):
    ##            file_miss_flag = True
    ##            with open('test_log.txt', 'a') as file:
    ##                file.write(f'\n{datetime.now()}\n')
    ##                file.write('cxx_outplans.json missed\n')

            if file_miss_flag == True:
                failed_list.append(cd_directory)
                #failed_test += 1
                with open(summary_file, 'a') as sumf:
                    sumf.write(f'case: {cd_directory} ----failed\n\n')
                    sumf.write(f'miss file\n')
                    sumf.write('\n')
                    
                continue

            result_au_py = compare(file_au, file_py, cd_directory, log_file, relative_tole, abs_tole, case_sensitive)
            #result_au_cxx = compare(file_au, file_cxx, cd_directory, log_file)
            #result_py_cxx = compare(file_py, file_cxx, cd_directory, log_file)

            case_fail_flag = False
            
            if result_au_py == 1:
                case_fail_flag = True

            if case_fail_flag == True:
                failed_list.append(cd_directory)
                #failed_test += 1
                with open(summary_file, 'a') as f:
                    f.write(f'case: {cd_directory} ----failed\n\n')
                    f.write(f'test failed\n')
                    f.write('\n')

                if result_au_py == 1:
                    with open(summary_file, 'a') as f:
                        f.write('output_plans.au.json -- output_plans.json  failed\n\n')

            elif case_fail_flag == False:
                passed_list.append(cd_directory)
                #successed_test += 1
                with open(summary_file, 'a') as f:
                    f.write(f'case: {cd_directory} ----passed\n\n')

        elif option == 'ca':
            
    ##        if not os.path.isfile(file_py):
    ##            file_miss_flag = True
    ##            with open('test_log.txt', 'a') as file:
    ##                file.write(f'\n{datetime.now()}\n')
    ##                file.write('output_plans.json missed\n')

            if not os.path.isfile(file_cxx):
                file_miss_flag = True
                with open('test_log.txt', 'a') as file:
                    file.write(f'\n{datetime.now()}\n')
                    file.write('cxx_outplans.json missed\n')

            if file_miss_flag == True:
                failed_list.append(cd_directory)
                #failed_test += 1
                with open(summary_file, 'a') as sumf:
                    sumf.write(f'case: {cd_directory} ----failed\n\n')
                    sumf.write(f'miss file\n')
                    sumf.write('\n')
                    
                continue

            #result_au_py = compare(file_au, file_py, cd_directory, log_file)
            result_au_cxx = compare(file_au, file_cxx, cd_directory, log_file, relative_tole, abs_tole, case_sensitive)
            #result_py_cxx = compare(file_py, file_cxx, cd_directory, log_file)

            case_fail_flag = False
            
            if result_au_cxx == 1:
                case_fail_flag = True

            if case_fail_flag == True:
                failed_list.append(cd_directory)
                #failed_test += 1
                with open(summary_file, 'a') as f:
                    f.write(f'case: {cd_directory} ----failed\n\n')
                    f.write(f'test failed\n')
                    f.write('\n')

                if result_au_cxx == 1:
                    with open(summary_file, 'a') as f:
                        f.write('output_plans.au.json -- cxx_outplans.json   failed\n\n')

            elif case_fail_flag == False:
                passed_list.append(cd_directory)
                #successed_test += 1
                with open(summary_file, 'a') as f:
                    f.write(f'case: {cd_directory} ----passed\n\n')



r = len(R) // cpu_count() + 1
n = r

index0 = 0
task_list = []
for i in range(cpu_count()):
    task_list.append(R[index0: n])
    index0 = n
    n = n + r

manager = Manager()
failed_list = manager.list()
passed_list = manager.list()

p = Pool(cpu_count())
for directory in task_list:
    p.apply_async(run_func, args=(directory, summary_file, failed_list, passed_list))

p.close()
p.join()


with open(summary_file, 'a') as f:
    f.write('\nTotal result:\n\n')
    f.write(f'total test: {len(R)}\n')
    f.write(f'passed:     {len(passed_list)}\n')
    f.write(f'failed:     {len(failed_list)}\n')
    
       
##    subprocess.call(['touch', 'new.txt'])
