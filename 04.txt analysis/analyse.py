# coding:utf8


def analysis(filename):
    s = open(filename,'r').read()
    num_chars = len(s)
    num_lines = s.count('\n')
    words = normalize(s).split()
    num_words = len(words)
    dic = {}
    for word in words:
        if word in dic:
            dic[word] += 1
        else:
            dic[word] = 1
    lis = dic.items()
    lis.sort(key = lambda item : item[1])
    lis = lis[-200:]
    lis.reverse()
    print lis
    print num_chars,num_lines,num_words

def normalize(s):
    '''delete spare characters not in keep'''
    keep = [chr(i) for i in range(ord('a'),ord('z')+1)]
    keep += [' ','-',"'"]
    result = ''
    for ch in s.lower():
        if ch in keep:
            result += ch
    return result

if __name__ == '__main__':
    analysis('bill.txt')