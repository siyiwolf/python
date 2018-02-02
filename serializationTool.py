import json
import os

import staticInfomation
import loadControlData
import loadFrame

classes = {
    'loadFrame' : loadFrame.loadFrame,
    'loadControlData' : loadControlData.loadControlData,
    'staticInfomation' : staticInfomation.staticInfomation
}
          
def serialize_instance(obj):
    d = { '__classname__' : type(obj).__name__ }
    d.update(vars(obj))
    return d

def unserialize_object(d):
    clsname = d.pop('__classname__', None)
    if  clsname:
        cls = serializationTool.classes[clsname]
        obj = cls.__new__(cls) # Make instance without calling __init__
        for key, value in d.items():
            setattr(obj, key, value)
            return obj
    else:
        return d

#序列化
def serialize_data(dir_name, obj):
    if  not os.path.exists(dir_name):
        os.makedirs(dir_name)

    file_name = dir_name + '\\file.json'
    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(obj, f)


#反序列化
def deserialize_data(dir_name):
    file_name = dir_name + '\\file.json'
    #判断是否存在文件
    if  os.path.exists(file_name):
        #进行反序列化
        with open('file_name', encoding='utf-8') as f:
            obj = json.load(f)
            return obj
    else:
        return None

