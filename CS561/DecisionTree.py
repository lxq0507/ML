import re
import pickle
import sys

def main():

    ＃创建决策树部分
    if sys.argv[1] == "CreateTree":
        print ("Creating a DecisionTree based on " + sys.argv[2])

        f = open(sys.argv[2],"r")
        line = f.readline()
        my_data = [];

        ＃按行读取文件，存储于list中
        while line:
            my_data.append(line)
            line = f.readline()

        f.close()

        ＃删除每行数据的tab键和换行键，将每一行的string分割成一个list
        for i in range (len(my_data)):
            my_data[i] = my_data[i][:-1]
            my_data[i] = re.split(r'\t+', my_data[i])

        for i in range(len(my_data)):
            for j in range(len(my_data[0])):
                my_data[i][j] = float(my_data[i][j])

        myTree = buildtree(my_data)

        prune(myTree, 0.1)

        printtree(myTree)
        storeTree(myTree, sys.argv[3])

        print ("Created and Stored the DecisionTree in " + sys.argv[3])

    ＃利用决策树进行分类
    if sys.argv[1] == "Classify":
        print (sys.argv[1] + " [" + sys.argv[3] + "] with Desicion Tree in " + sys.argv[2])
        fr = open(sys.argv[2], 'rb')
        myTree = pickle.load(fr)

        fr.close()

        ＃将待分类数据存于list中
        classifyArray = sys.argv[3].split(',')
        for i in range(len(classifyArray)):
            classifyArray[i] = float(classifyArray[i])

        result = classify(classifyArray, myTree)

        for k,v in result.items():
            print ("Classify Result : " + str(int(k)))


# 对y的各种可能的取值出现的个数进行计数.。其他函数利用该函数来计算数据集和的混杂程度
def uniquecounts(rows):
    results = {}
    for row in rows:
        #计数结果在最后一列
        r = row[len(row)-1]
        if r not in results:results[r] = 0
        results[r]+=1
    return results # 返回一个字典


# 熵


def entropy(rows):
    from math import log
    log2 = lambda x:log(x)/log(2)
    results = uniquecounts(rows)
    #开始计算熵的值
    ent = 0.0
    for r in results.keys():
        p = float(results[r])/len(rows)
        ent = ent - p*log2(p)
    return ent


#定义节点的属性
class decisionnode:
    def __init__(self,col = -1,value = None, results = None, tb = None,fb = None):
        self.col = col   # col是待检验的判断条件所对应的列索引值
        self.value = value # value对应于为了使结果为True，当前列必须匹配的值
        self.results = results #保存的是针对当前分支的结果，它是一个字典
        self.tb = tb ## desision node,对应于结果为true时，树上相对于当前节点的子树上的节点
        self.fb = fb ## desision node,对应于结果为true时，树上相对于当前节点的子树上的节点



#在某一列上对数据集进行拆分。可应用于数值型或因子型变量
def divideset(rows,column,value):
    #定义一个函数，判断当前数据行属于第一组还是第二组
    split_function = None
    if isinstance(value,int) or isinstance(value,float):
        split_function = lambda row:row[column] >= value
    else:
        split_function = lambda row:row[column]==value
    # 将数据集拆分成两个集合，并返回
    set1 = [row for row in rows if split_function(row)]
    set2 = [row for row in rows if not split_function(row)]
    return(set1,set2)


# 以递归方式构造树

def buildtree(rows,scoref = entropy):
    if len(rows)==0 : return decisionnode()
    current_score = scoref(rows)

    # 定义一些变量以记录最佳拆分条件
    best_gain = 0.0
    best_criteria = None
    best_sets = None

    column_count = len(rows[0]) - 1
    for col in range(0,column_count):
        #在当前列中生成一个由不同值构成的序列
        column_values = {}
        for row in rows:
            column_values[row[col]] = 1 # 初始化
        #根据这一列中的每个值，尝试对数据集进行拆分
        for value in column_values.keys():
            (set1,set2) = divideset(rows,col,value)

            # 信息增益
            p = float(len(set1))/len(rows)
            gain = current_score - p*scoref(set1) - (1-p)*scoref(set2)
            if gain>best_gain and len(set1)>0 and len(set2)>0:
                best_gain = gain
                best_criteria = (col,value)
                best_sets = (set1,set2)

    #创建子分支
    if best_gain>0:
        trueBranch = buildtree(best_sets[0])  #递归调用
        falseBranch = buildtree(best_sets[1])
        return decisionnode(col = best_criteria[0],value = best_criteria[1],
                            tb = trueBranch,fb = falseBranch)
    else:
        return decisionnode(results = uniquecounts(rows))

def prune(tree,mingain):
    # 如果分支不是叶节点，则对其进行剪枝
    if tree.tb.results == None:
        prune(tree.tb,mingain)
    if tree.fb.results == None:
        prune(tree.fb,mingain)
    # 如果两个子分支都是叶节点，判断是否能够合并
    if tree.tb.results !=None and tree.fb.results !=None:
        #构造合并后的数据集
        tb,fb = [],[]
        for v,c in tree.tb.results.items():
            tb+=[[v]]*c
        for v,c in tree.fb.results.items():
            fb+=[[v]]*c
        #检查熵的减少量
        p = float(len(tb))/len(tb+fb)
        delta = entropy(tb+fb)- p*entropy(tb) - (1 - p)*entropy(fb)
        if delta < mingain:
            # 合并分支
            tree.tb,tree.fb = None,None
            tree.results = uniquecounts(tb+fb)

#存储
def storeTree(inputTree, filename):
    import pickle
    fw = open(filename, 'wb') #以二进制读写方式打开文件
    pickle.dump(inputTree, fw)  #pickle.dump(对象, 文件，[使用协议])。序列化对象
    # 将要持久化的数据“对象”，保存到“文件”中，使用有3种，索引0为ASCII，1是旧式2进制，2是新式2进制协议，不同之处在于后者更高效一些。
    #默认的话dump方法使用0做协议
    fw.close() #关闭文件


# 决策树的显示
def printtree(tree,indent = ''):
    # 是否是叶节点
    if tree.results!=None:
        print (str(tree.results))
    else:
        # 打印判断条件
        print (str(tree.col)+":"+str(tree.value)+"? ")
        #打印分支
        print (indent+"T->")
        printtree(tree.tb,indent+" ")
        print (indent+"F->")
        printtree(tree.fb,indent+" ")


# 对新的观测数据进行分类


def classify(observation,tree):
    if tree.results!= None:
        return tree.results
    else:
        v = observation[tree.col]
        branch = None
        if isinstance(v,int) or isinstance(v,float):
            if v>= tree.value: branch = tree.tb
            else: branch = tree.fb
        else:
            if v==tree.value : branch = tree.tb
            else: branch = tree.fb
        return classify(observation,branch)

if __name__=="__main__":
    main()
