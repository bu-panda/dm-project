import os  
allFileNum = 0

# @level show the depth of current folder. Start with 0
# @path begin path
# @rs save the detail file path
def printPath(level, path, rs):  
    global allFileNum  

    dirList = []  
    fileList = []  
    files = os.listdir(path)  
    dirList.append(str(level))  
    for f in files:  
        if(os.path.isdir(path + '/' + f)):  
            if(f[0] == '.'):  
                pass  
            else:  
                dirList.append(f)  
        if(os.path.isfile(path + '/' + f)):  
            fileList.append(f)

            if f != '.DS_Store':
            
                rs.append(path+'/'+f)
    i_dl = 0  
    for dl in dirList:  
        if(i_dl == 0):  
            i_dl = i_dl + 1  
        else:  
            #print '-' * (int(dirList[0])), dl  
            printPath((int(dirList[0]) + 1), path + '/' + dl,rs)  

# @dirpath the root path to travel through
# @output_path str where you save the result
def getAllFileNames(dirpath, output_path):
    file_names = []
    printPath(1, dirpath, file_names)  
    f = open(output_path,'w')
    for each in file_names:
        f.write(each+'\n')
    f.close()

# @filepath str raw data file path
# @container TYPE is file. You should open a file with 'a' mode to save the
#   result without covering previous information
# @space_save. If True, when finishing processing one file,
#   delete it to save space

def processFile(filepath, container, space_save=True):

    filenames = open(filepath)
    i = 0
    for each_name in filenames:
        try:
            each_name = each_name.strip()
            data = open(each_name)
            root, year,name = each_name.split('/')

            # read header line
            data.readline()
            for eachline in data:
                info = eachline.strip().split(' ')
                info = [x for x in info if x != '']
                r = ','.join(info)
                container.write(r+'\n')
            i += 1
            data.close()
            if space_save:
                order = 'rm '+each_name
                os.system(order)
            if i % 100 == 0:
                
                print i,' files parse successfully'
        except ValueError:
            print 'ecounter value problems when processing: ', each_name
            continue
        except IOError:
            print 'IOError when processing:'. each_name
            continue

# Use the file that contains stations' location information to build
# a dictionary, key is station_id, value is a list [latitude, logitude]
def buildStationInfo(location_file):
    loc_file = open(location_file)
    rs = {}
    for eachline in loc_file:

        info = eachline.strip().split(' ')
        info = [x for x in info if x != '']

        if len(info) < 3:
            continue
        lat = info[-3]
        log = info[-2]
        station_id = int(info[0])
        if verify(lat, log):
            rs[station_id] = [lat, log]
    return rs

# check whether location information is well-formed
def verify(lat, log):
    c1 = lat[-1]
    c2 = log[-1]

    v1 = (c1 == 'N' or c1 == 'S')
    v2 = (c2 == 'E' or c2 == 'W')
    return v1 and v2

    
    
# SQL join based on station_id
def joinData(data_path, output_path,location_dict):

    f = open(data_path)
    fin = open(output_path, 'w')
    for each in f:
        info = each.strip().split(',')
        station_id = int(info[0])

        loc_info = location_dict.get(station_id, None)
        if loc_info:
            info.append(loc_info[0])
            info.append(loc_info[1])
            r = ",".join(info)
            fin.write(r+'\n')
    f.close()
    fin.close()

    
# If you don't want to work on the whole data file
# Here is the method to filt data by year.
# @filepath raw data file
# @year you want which year
# @output_path where you want to save your new file
def filtDataByYear(filepath,year,output_path):
    f = open(filepath)
    fin = open(output_path,'w')
    i =0
    for each in f:
        info = each.strip().split(',')
        timestamp = info[2]
        y = int(timestamp[0:4])
        if y == year:
            i+=1
            fin.write(each)
    print 'total ', i, ' records'
    f.close()
    fin.close()
    

# Write your own code here if you want to do sth on data file
if __name__ == '__main__':
    d = buildStationInfo('station.txt')
    filtDataByYear('merge.txt', 2006, 'sample.csv')
    joinData('sample.csv','data_with_location.csv',d)
    print 'done'
'''
    getAllFileNames('gsod', 'files.txt')
    print 'file name done'
    container = open('merge.txt','a')
    processFile('files.txt', container)
    container.close()
'''
