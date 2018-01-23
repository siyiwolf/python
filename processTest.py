from multiprocessing import Pool
import os, time, random

i_max = 1

def assign_worker(level = 0):
    if level > i_max:
        return

    print('Done parse')
    print('ClassFly')
    print('LoadFile')
    p = Pool(4)
    for i in range(4):
        p.apply_async(long_time_task, args=(i,))

    for i in range(4):
        assign_worker(level + 1)
    print('Waiting for all subprocesses done...')
    p.close()
    p.join()
    print('All subprocesses done.')

def long_time_task(name):
    print('Run task %s (%s)...' % (name, os.getpid()))
    start = time.time()
    time.sleep(random.random() * 3)
    end = time.time()
    print('Task %s runs %0.2f seconds.' % (name, (end - start)))

if __name__=='__main__':
    print('Parent process %s.' % os.getpid())
    assign_worker(0)
    print('Parent process end.')
    input()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

##from multiprocessing import Pool
##import os, time, random
##
##def long_time_task(name):
##    print('Run task %s (%s)...' % (name, os.getpid()))
##    start = time.time()
##    time.sleep(random.random() * 3)
##    end = time.time()
##    print('Task %s runs %0.2f seconds.' % (name, (end - start)))
##
##if __name__=='__main__':
##    print('Parent process %s.' % os.getpid())
##    p = Pool(4)
##    for i in range(5):
##        p.apply_async(long_time_task, args=(i,))
##    print('Waiting for all subprocesses done...')
##    p.close()
##    p.join()
##    print('All subprocesses done.')
##    input()
##    
