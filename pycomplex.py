from importlib.resources import path
from multiprocessing import current_process
import datetime
import logging
import errno
import psutil
import os


def makeLog(ymd):
    # current_directory_path = '/'.join(os.path.realpath(__file__).split('/')[:-1])
    # current_directory_path = (os.path.realpath(__file__).split(os.path.sep)[:-1])
    # os.curdir
    current_directory_path = os.path.split(os.path.realpath(__file__))[:-1]
    path_log = os.path.join(os.curdir, "log")
    
    print(current_directory_path)

    mylogger = logging.getLogger("complex")
    mylogger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    stream_hander = logging.StreamHandler()
    stream_hander.setFormatter(formatter)
    mylogger.addHandler(stream_hander)

    try:
        if not(os.path.isdir(path_log)):
            os.makedirs(path_log)
    except OSError as e:
        if e.errno != errno.EEXIST:
            print("Failed to create directory!!!!!")
            raise

    file_handler = logging.FileHandler(os.path.join(path_log, f"{ymd}_pycomplex.log"))
    mylogger.addHandler(file_handler)

    return mylogger


def check_time_memory_core(func, *args, **kwargs):
    before_pid = os.getpid()
    before_memory_usage_dict = dict(psutil.virtual_memory()._asdict())
    before_memory_usage_percent = before_memory_usage_dict['percent']
    before_cpu_percent = psutil.cpu_percent()
    before_current_process = psutil.Process(before_pid)
    before_current_process_memory_usage_as_KB = before_current_process.memory_info()[0] / 2.**20
    time_start = datetime.datetime.now()

    result = func(*args, **kwargs)

    time_end = datetime.datetime.now()
    after_pid = os.getpid()
    after_memory_usage_dict = dict(psutil.virtual_memory()._asdict())
    after_memory_usage_percent = after_memory_usage_dict['percent']
    after_cpu_percent = psutil.cpu_percent()
    after_current_process = psutil.Process(after_pid)
    after_current_process_memory_usage_as_KB = before_current_process.memory_info()[0] / 2.**20
    
    dict_log = {
        "before": {
            "pid"                                   : before_pid,
            "time_start"                            : time_start,
            "cpu_percent"                           : before_cpu_percent,
            "memory_usage_percent"                  : before_memory_usage_percent,
            "current_process"                       : before_current_process,
            "current_process_memory_usage_as_KB"    : before_current_process_memory_usage_as_KB
        },
        "after": {
            "pid"                                   : after_pid,
            "time_end"                              : time_end,
            "running_time"                          : time_end - time_start,
            "cpu_percent"                           : after_cpu_percent,
            "memory_usage_percent"                  : after_memory_usage_percent,
            "current_process"                       : after_current_process,
            "current_process_memory_usage_as_KB"    : after_current_process_memory_usage_as_KB
        }
    }
    
    return dict_log, result


def check_time_memory_print(func, *args, **kwargs):
    dict_log, result = check_time_memory_core(func, *args, **kwargs)

    print("=============== Function Info =================")
    print(f"func               : {str(func).split()[1]:>26s}")
    print(f"args               : {str(args):>26s}")
    print("=============== Before Function ===============")
    print(f"Start Time         : {dict_log['before']['time_start'].strftime('%Y-%m-%d %H:%M:%S.%f')}")
    print(f"CPU percent        : {dict_log['before']['cpu_percent']: 23.3f}  %")
    print(f"Memory percent     : {dict_log['before']['memory_usage_percent']: 23.3f}  %")
    print(f"Current memory KB  : {dict_log['before']['current_process_memory_usage_as_KB']: 23.3f} KB")
    print("=============== After Function ================")
    print(f"End Time           : {dict_log['after']['time_end'].strftime('%Y-%m-%d %H:%M:%S.%f')}")
    print(f"Running Time       :             {dict_log['after']['running_time']}")
    print(f"CPU percent        : {dict_log['after']['cpu_percent']: 23.3f}  %")
    print(f"Memory percent     : {dict_log['after']['memory_usage_percent']: 23.3f}  %")
    print(f"Current memory KB  : {dict_log['after']['current_process_memory_usage_as_KB']: 23.3f} KB")
    print("===============================================")


def check_time_memory_log(func, *args, **kwargs):
    mylogger = makeLog(datetime.datetime.now().strftime("%Y%m%d"))

    dict_log, result = check_time_memory_core(func, *args, **kwargs)

    # i = ("=============== function info =================\n"
    #      f"func               : {str(func).split()[1]:>26s}\n"
    #      f"args               : {str(args):>26s}\n"
    #      "=============== Before function ===============\n"
    #      f"Start Time         : {dict_log['before']['time_start'].strftime('%Y-%m-%d %H:%M:%S.%f')}\n"
    #      f"CPU percent        : {dict_log['before']['cpu_percent']: 23.3f}  %\n"
    #      f"Memory percent     : {dict_log['before']['memory_usage_percent']: 23.3f}  %\n"
    #      f"Current memory KB  : {dict_log['before']['current_process_memory_usage_as_KB']: 23.3f} KB\n"
    #      "=============== After function ================\n"
    #      f"End Time           : {dict_log['after']['time_end'].strftime('%Y-%m-%d %H:%M:%S.%f')}\n"
    #      f"Running Time       :             {dict_log['after']['running_time']}\n"
    #      f"CPU percent        : {dict_log['after']['cpu_percent']: 23.3f}  %\n"
    #      f"Memory percent     : {dict_log['after']['memory_usage_percent']: 23.3f}  %\n"
    #      f"Current memory KB  : {dict_log['after']['current_process_memory_usage_as_KB']: 23.3f} KB\n"
    #      "===============================================\n")

    # mylogger.info(i)
    
    mylogger.info("=============== Function Info =================")
    mylogger.info(f"func               : {str(func).split()[1]:>26s}")
    mylogger.info(f"args               : {str(args):>26s}")
    mylogger.info("=============== Before Function ===============")
    mylogger.info(f"Start Time         : {dict_log['before']['time_start'].strftime('%Y-%m-%d %H:%M:%S.%f')}")
    mylogger.info(f"CPU percent        : {dict_log['before']['cpu_percent']: 23.3f}  %")
    mylogger.info(f"Memory percent     : {dict_log['before']['memory_usage_percent']: 23.3f}  %")
    mylogger.info(f"Current memory KB  : {dict_log['before']['current_process_memory_usage_as_KB']: 23.3f} KB")
    mylogger.info("=============== After Function ================")
    mylogger.info(f"End Time           : {dict_log['after']['time_end'].strftime('%Y-%m-%d %H:%M:%S.%f')}")
    mylogger.info(f"Running Time       :             {dict_log['after']['running_time']}")
    mylogger.info(f"CPU percent        : {dict_log['after']['cpu_percent']: 23.3f}  %")
    mylogger.info(f"Memory percent     : {dict_log['after']['memory_usage_percent']: 23.3f}  %")
    mylogger.info(f"Current memory KB  : {dict_log['after']['current_process_memory_usage_as_KB']: 23.3f} KB")
    mylogger.info("===============================================")

    
if __name__ == "__main__":
    def exam1(count):
        odd = list()
        even = list()
        
        for i in range(count):
            if i % 2:
                odd.append(i)
            else:
                even.append(i)
                
        return odd, even
        
    check_time_memory_log(exam1, 10**7)
    check_time_memory_print(exam1, 10**7)
    