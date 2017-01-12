#-*- coding: utf-8 -*-

class Solution(object):
    def findLadders(self, beginWord, endWord, wordlist):
        """
        :type beginWord: str
        :type endWord: str
        :type wordlist: Set[str]
        :rtype: List[List[int]]
        """
        if beginWord == endWord:
            return [beginWord]

        distance_list = self.initDistanceist(beginWord, endWord, wordlist)
        begin_idx = 0
        end_idx = len(distance_list) - 1

        solved, distance_list, begin_idx, end_idx = self.checkDistanceist(distance_list, begin_idx, end_idx)

        while not solved and begin_idx < end_idx:
            solved, distance_list, begin_idx, end_idx = self.checkDistanceist(distance_list, begin_idx, end_idx)

        return self.fixSolution(solved) if solved else []

    def fixSolution(self, solved):
        fix_set = set()
        result = []
        for res in solved:
            key = ','.join(res)
            if key not in fix_set:
                result.append(res)
                fix_set.add(key)
        return result

    def solutionDistanceist(self, solved, distance_list, begin_idx, end_idx):
        ret = []
        for tag in solved:
            for begin_from in distance_list[begin_idx][tag][1]:
                for end_from in distance_list[end_idx][tag][1]:
                    ret.append(begin_from + [tag] + end_from[::-1])
        return ret

    def checkDistanceist(self, distance_list, begin_idx, end_idx):
        result = []

        begin_tag_all = set(distance_list[begin_idx].keys())
        end_tag_all = set(distance_list[end_idx].keys())
        begin_reachable_all, distance_list = self.reachableDistanceist(distance_list, begin_idx, begin_idx + 1)

        begin_tmp = end_tag_all & begin_reachable_all
        if begin_tmp:
            result.extend(self.solutionDistanceist(begin_tmp, distance_list, begin_idx + 1, end_idx))

        end_reachable_all, distance_list = self.reachableDistanceist(distance_list, end_idx, end_idx - 1)
        end_tmp = begin_tag_all & end_reachable_all
        if end_tmp:
            result.extend(self.solutionDistanceist(end_tmp, distance_list, begin_idx, end_idx - 1))

        if result:
            return result, distance_list, begin_idx + 1, end_idx - 1

        join_tmp = begin_reachable_all & end_reachable_all
        if join_tmp:
            result.extend(self.solutionDistanceist(join_tmp, distance_list, begin_idx + 1, end_idx - 1))

        return result, distance_list, begin_idx + 1, end_idx - 1

    def reachableDistanceist(self, distance_list, this_idx, next_idx):
        this_reachable_all = []
        this_dict = distance_list[this_idx]
        next_dict = distance_list[next_idx]
        for this_tag, item in this_dict.items():
            for tag in item[0]:
                if _distance(tag, this_tag) == 1:
                    this_reachable_all.append(tag)
                    allow_ = set(item[0])
                    allow_.remove(tag)
                    if tag in next_dict:
                        next_dict[tag] = (next_dict[tag][0] | allow_, next_dict[tag][1] + [from_ + [this_tag] for from_ in item[1]])
                    else:
                        next_dict[tag] = (allow_, [from_ + [this_tag] for from_ in item[1]])
        return set(this_reachable_all), distance_list

    def initDistanceist(self, beginWord, endWord, wordlist):
        return [
            {beginWord: (set(list(wordlist) + [endWord]), [[], ])}] + \
            [{} for _ in wordlist] + \
            [{endWord: (set(list(wordlist) + [beginWord]), [[], ])}
        ]


def _distance(str1, str2):
    if str2 < str1:
        return _distance(str2, str1)

    distance = 0
    for idx, char in enumerate(str1):
        if str2[idx] != char:
            distance += 1
    return distance

class Solution2:
    # @param start, a string
    # @param end, a string
    # @param dict, a set of string
    # @return a list of lists of string
    def findLadders(self, start, end, dict):
        def buildpath(path, word): # path is a list; word is a string
            if len(prevMap[word])==0: #prevMap: dict  #Blank prevMap means all the node in the path is visited
                path.append(word);
                currPath=path[:]   # hard copy path to currPath. No link between pat and currPath
                currPath.reverse();
                result.append(currPath)
                path.pop(); #remove the end element
                return
            path.append(word)
            for iter in prevMap[word]: # reverse the path,
                buildpath(path, iter)
            path.pop()

        result=[]
        prevMap={} # prevMap is a dict
        length=len(start)
        for i in dict: #dict: is a set
            prevMap[i]=[] # set the value for each key as blank string
        candidates=[set(),set()]; current=0; previous=1
        candidates[current].add(start) # set0 add start
        while True:
            current, previous=previous, current           #下一次循环开始时，上一次循环的candidates[current]变成了candidates[previous]，而上一次循环的candidates[previous]变成了candidates[current]并清空
            for i in candidates[previous]: dict.remove(i) #先将candidates[previous]中的单词（前一层的单词）在dict中删除
            candidates[current].clear()                   #再将candidates[current]清空
            for word in candidates[previous]:             #再据candidates[previous]中的单词寻找下一层的单词
                for i in range(length):
                    part1=word[:i]; part2=word[i+1:]
                    for j in 'abcdefghijklmnopqrstuvwxyz':
                        if word[i]!=j:
                            nextword=part1+j+part2
                            if nextword in dict:
                                candidates[current].add(nextword) #将下一层存入candidates[current]中
                                prevMap[nextword].append(word)    #同时将单词存入前驱单词表中
            if len(candidates[current])==0: return result         #当集合为空,返回结果
            if end in candidates[current]: break #当循环中的candidates[current]中出现了end单词时，说明我们的路径已经找出来了，工作完成了。
        buildpath([], end) #重建每一条路径。prevMap is a dict，这个prevMap可以使用DFS来重建每一条路径。
        return result

############################
########### TEST ###########
############################

def test(beginWord, endWord, wordList, ret):
    ret_set = set([','.join(res) for res in ret])
    ans = Solution().findLadders(beginWord, endWord, set(wordList))
    ans_set = set([','.join(res) for res in ans])
    print ret_set == ans_set, ans if ret_set == ans_set else ('less' if len(ans)<len(ret) else 'more', ret_set.difference(ans_set))

def main():
    beginWord = "hit"
    endWord = "cog"
    wordList = ["hot","dot","dog","lot","log"]
    ret = [["hit","hot","dot","dog","cog"], ["hit","hot","lot","log","cog"]]
    test(beginWord, endWord, wordList, ret)

    beginWord = "red"
    endWord = "tax"
    wordList = ["ted","tex","red","tax","tad","den","rex","pee"]
    ret = [["red","ted","tad","tax"],["red","ted","tex","tax"],["red","rex","tex","tax"]]
    test(beginWord, endWord, wordList, ret)

    beginWord = "a"
    endWord = "c"
    wordList = ["a","b","c"]
    ret = [["a","c"]]
    test(beginWord, endWord, wordList, ret)

    beginWord = "cat"
    endWord = "fin"
    wordList = ["ion","rev","che","ind","lie","wis","oct","ham","jag","ray","nun","ref","wig","jul","ken","mit","eel","paw","per","ola","pat","old","maj","ell","irk","ivy","beg","fan","rap","sun","yak","sat","fit","tom","fin","bug","can","hes","col","pep","tug","ump","arc","fee","lee","ohs","eli","nay","raw","lot","mat","egg","cat","pol","fat","joe","pis","dot","jaw","hat","roe","ada","mac"]
    ret = [["cat","fat","fit","fin"],["cat","fat","fan","fin"],["cat","can","fan","fin"]]
    test(beginWord, endWord, wordList, ret)

    beginWord = "cet"
    endWord = "ism"
    wordList = ["kid","tag","pup","ail","tun","woo","erg","luz","brr","gay","sip","kay","per","val","mes","ohs","now","boa","cet","pal","bar","die","war","hay","eco","pub","lob","rue","fry","lit","rex","jan","cot","bid","ali","pay","col","gum","ger","row","won","dan","rum","fad","tut","sag","yip","sui","ark","has","zip","fez","own","ump","dis","ads","max","jaw","out","btu","ana","gap","cry","led","abe","box","ore","pig","fie","toy","fat","cal","lie","noh","sew","ono","tam","flu","mgm","ply","awe","pry","tit","tie","yet","too","tax","jim","san","pan","map","ski","ova","wed","non","wac","nut","why","bye","lye","oct","old","fin","feb","chi","sap","owl","log","tod","dot","bow","fob","for","joe","ivy","fan","age","fax","hip","jib","mel","hus","sob","ifs","tab","ara","dab","jag","jar","arm","lot","tom","sax","tex","yum","pei","wen","wry","ire","irk","far","mew","wit","doe","gas","rte","ian","pot","ask","wag","hag","amy","nag","ron","soy","gin","don","tug","fay","vic","boo","nam","ave","buy","sop","but","orb","fen","paw","his","sub","bob","yea","oft","inn","rod","yam","pew","web","hod","hun","gyp","wei","wis","rob","gad","pie","mon","dog","bib","rub","ere","dig","era","cat","fox","bee","mod","day","apr","vie","nev","jam","pam","new","aye","ani","and","ibm","yap","can","pyx","tar","kin","fog","hum","pip","cup","dye","lyx","jog","nun","par","wan","fey","bus","oak","bad","ats","set","qom","vat","eat","pus","rev","axe","ion","six","ila","lao","mom","mas","pro","few","opt","poe","art","ash","oar","cap","lop","may","shy","rid","bat","sum","rim","fee","bmw","sky","maj","hue","thy","ava","rap","den","fla","auk","cox","ibo","hey","saw","vim","sec","ltd","you","its","tat","dew","eva","tog","ram","let","see","zit","maw","nix","ate","gig","rep","owe","ind","hog","eve","sam","zoo","any","dow","cod","bed","vet","ham","sis","hex","via","fir","nod","mao","aug","mum","hoe","bah","hal","keg","hew","zed","tow","gog","ass","dem","who","bet","gos","son","ear","spy","kit","boy","due","sen","oaf","mix","hep","fur","ada","bin","nil","mia","ewe","hit","fix","sad","rib","eye","hop","haw","wax","mid","tad","ken","wad","rye","pap","bog","gut","ito","woe","our","ado","sin","mad","ray","hon","roy","dip","hen","iva","lug","asp","hui","yak","bay","poi","yep","bun","try","lad","elm","nat","wyo","gym","dug","toe","dee","wig","sly","rip","geo","cog","pas","zen","odd","nan","lay","pod","fit","hem","joy","bum","rio","yon","dec","leg","put","sue","dim","pet","yaw","nub","bit","bur","sid","sun","oil","red","doc","moe","caw","eel","dix","cub","end","gem","off","yew","hug","pop","tub","sgt","lid","pun","ton","sol","din","yup","jab","pea","bug","gag","mil","jig","hub","low","did","tin","get","gte","sox","lei","mig","fig","lon","use","ban","flo","nov","jut","bag","mir","sty","lap","two","ins","con","ant","net","tux","ode","stu","mug","cad","nap","gun","fop","tot","sow","sal","sic","ted","wot","del","imp","cob","way","ann","tan","mci","job","wet","ism","err","him","all","pad","hah","hie","aim","ike","jed","ego","mac","baa","min","com","ill","was","cab","ago","ina","big","ilk","gal","tap","duh","ola","ran","lab","top","gob","hot","ora","tia","kip","han","met","hut","she","sac","fed","goo","tee","ell","not","act","gil","rut","ala","ape","rig","cid","god","duo","lin","aid","gel","awl","lag","elf","liz","ref","aha","fib","oho","tho","her","nor","ace","adz","fun","ned","coo","win","tao","coy","van","man","pit","guy","foe","hid","mai","sup","jay","hob","mow","jot","are","pol","arc","lax","aft","alb","len","air","pug","pox","vow","got","meg","zoe","amp","ale","bud","gee","pin","dun","pat","ten","mob"]
    ret = [['cet', 'cat', 'can', 'ian', 'inn', 'ins', 'its', 'ito', 'ibo', 'ibm', 'ism'], ['cet', 'cot', 'con', 'ion', 'inn', 'ins', 'its', 'ito', 'ibo', 'ibm', 'ism'], ['cet', 'get', 'gee', 'gte', 'ate', 'ats', 'its', 'ito', 'ibo', 'ibm', 'ism']]
    test(beginWord, endWord, wordList, ret)


if __name__ == '__main__':
    main()
    pass