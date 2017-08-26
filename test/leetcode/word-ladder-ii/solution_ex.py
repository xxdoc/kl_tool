#-*- coding: utf-8 -*-

class Solution(object):
    def findLadders(self, beginWord, endWord, wordlist):
        """
        :type beginWord: str
        :type endWord: str
        :type wordlist: List[str]
        :rtype: List[List[str]]
        """
        wordlist = set(wordlist)
        ALL_CHAR = "abcdefghijklmnopqrstuvwxyz"
        solved, solved_len, reachable, range_ = {beginWord: [[beginWord]], endWord: []}, {beginWord: 1}, [beginWord, ], range(len(beginWord))
        append_and_copy = lambda item_list, add: [item + [add] for item in item_list]
        _newword = lambda prev: (prev[:i] + j + prev[i + 1:] for i in range_ for j in ALL_CHAR if prev[i] != j)

        while reachable:
            prev = reachable.pop(0)
            for newword in _newword(prev):
                if newword == endWord:
                    solved[endWord] = append_and_copy(solved[prev], endWord)
                    max_len = len(solved[endWord][0])
                    while reachable:
                        prev_ = reachable.pop(0)
                        if solved_len[prev_] < max_len:
                            for newword_ in _newword(prev_):
                                newword_ == endWord  and solved[endWord].extend(append_and_copy(solved[prev_], endWord))
                    break
                if newword in wordlist:
                    reachable.append(newword)
                    solved[newword] = append_and_copy(solved[prev], newword)
                    solved_len[newword] = len(solved[newword][0])
                    wordlist.remove(newword)
                elif newword in solved and solved_len[newword] == solved_len[prev] + 1:
                    solved[newword].extend(append_and_copy(solved[prev], newword))
        return solved[endWord]

############################
########### TEST ###########
############################

def test(beginWord, endWord, wordList, ret):
    ret_set = set([','.join(res) for res in ret])
    ans = Solution().findLadders(beginWord, endWord, set(wordList))
    ans_set = set([','.join(res) for res in ans])
    log_str = (len(ret_set)  if ret_set == ans_set else ('less' if len(ans)<len(ret) else 'more', ret_set.difference(ans_set)))
    print ret_set == ans_set, ans, log_str
    if ret_set != ans_set:
        raise AssertionError('[ERROR] beginWord:%s, endWord:%s, log:%s, ret:%r' % (beginWord, endWord, log_str, ret))

def main():
    beginWord = "a"
    endWord = "c"
    wordList = ["a","b","c"]
    ret = [["a","c"]]
    test(beginWord, endWord, wordList, ret)

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