# coding = UTF-8  
import re
import os

class staticInfomation():
    def __init__(self, current_dir):
        self.son_list = list()
        self.file_num = 0
        self.failed_num = 0
        self.current_dir = current_dir

    def get_current_dir(self):
        return self.current_dir

    def get_file_dir(self, file_type):
        file_path =self.current_dir + '\\' + file_type[1:] + '_file'
        return file_path

    def get_sub_dir(self, level, index):
        sub_path = self.current_dir + '\\' + str(level) + '_' + str(index)
        return sub_path

    def set_file_num(self, file_num):
        self.file_num = file_num

    def get_file_num(self):
        return self.file_num

    def static_sum_num(self):
        sumNum = self.file_num;
        for son_static in self.son_list:
            sumNum += son_static.static_sum_num()

        return sumNum

    def static_failed_sum(self):
        sumFailedNum = self.failed_num;
        for son_static in self.son_list:
            sumFailedNum += son_static.static_failed_sum()

        return sumFailedNum

    def updata_failed_num(self):
        self.failed_num += 1;
        
    def set_failed_num(self, failed_num):
        self.failed_num = failed_num;

    def add_son_static_data(self, son_data):
        self.son_list.append(son_data)

    def __str__(self):
        static_info = 'The static information is' +  '\n' +\
                      'Num of Sons:' + str(len(self.son_list)) + '\n' +\
                      'File Num:' + str(self.file_num) + '\n' +\
                      'Sum File Num:' + str(self.static_sum_num()) + '\n' +\
                      'Failed Num:' + str(self.failed_num) + '\n' +\
                      'Failed Sum Num:' + str(self.static_failed_sum())
        return static_info
    

    
        

