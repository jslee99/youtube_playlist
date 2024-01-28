
#crawling_playlist에 종속
# \t으로 구분하는 것, 파일 밑에 개수 써놓는 것 등등

# old : 이전 통합본
# new : 이번에 새로 크롤링한 파일
old_file_name = '팝송가사 2023 03.txt'
new_file_name = '팝송가사 2024 01.txt'
oldComprehensiveMusic = {}
newMusic = {}

def fileToDic(fileName : str, dic : dict):
    file = open('./' + fileName, 'r', encoding='utf-8')
    lines = file.readlines()
    for line in lines:
        key_value_list = line.split('\t')
        if(len(key_value_list) != 2): # 끝에 도달했을때, 즉 \n을 만나면 break
            break;
        key = key_value_list[0]
        value = key_value_list[1].strip('\n')
        if(dic.get(key) != None): # 파일 내에 같은 노래가 들어가 있는 경우, 거의 없을듯?
            print(fileName)
            raise Exception(str(key_value_list) + ' duplicate key')
        dic[key] = value # dict에 요소 추가
    file.close();
        
def findRemovedMusic(oldComprehensiveMusic : dict, newMusic : dict):
    removedMusic = {}
    for key in oldComprehensiveMusic.keys():
        if(newMusic.get(key) == None):
            removedMusic[key] = oldComprehensiveMusic.get(key)
    return removedMusic

def removedMusicToFile(removedMusic : dict):
    file = open('./removedMusic.txt', 'a', encoding='utf-8')
    for key in removedMusic.keys():
        file.write(key)
        file.write('\t')
        file.write(removedMusic.get(key))
        file.write('\n')
    file.close()
    
def mergeDicToFile(oldComprehensiveMusic : dict, newMusic : dict):
    file = open('./comprehesive.txt', 'a', encoding='utf-8')
    cnt = 0
    for key in oldComprehensiveMusic.keys():
        file.write(key)
        file.write('\t')
        file.write(oldComprehensiveMusic.get(key))
        file.write('\n')
        cnt += 1
    for key in newMusic.keys():
        if(oldComprehensiveMusic.get(key) != None):
            continue
        file.write(key)
        file.write('\t')
        file.write(newMusic.get(key))
        file.write('\n')
        cnt += 1
    file.write('\n')
    file.write('\n')
    file.write(str(cnt))
    file.close()
        

if __name__ == '__main__':
    fileToDic(old_file_name, oldComprehensiveMusic)
    fileToDic(new_file_name, newMusic)
    removedMusic = findRemovedMusic(oldComprehensiveMusic, newMusic)
    removedMusicToFile(removedMusic)
    mergeDicToFile(oldComprehensiveMusic, newMusic)
        