#### 面试题目
1.简述__new__和__init__的区别

    创建一个新实例时调用__new__,初始化一个实例时用__init__,这是它们最本质的区别。

    new方法会返回所构造的对象，init则不会.

    new函数必须以cls作为第一个参数，而init则以self作为其第一个参数.
    
    
#### 编程题目
1.在一个二维数组中，每一行都按照从左到右递增的顺序排序，每一列都按照从上到下递增的顺序排序。请完成一个函数，输入这样的一个二维数组和一个整数，判断数组中是否含有该整数。

        arr = [[1,4,7,10,15], [2,5,8,12,19], [3,6,9,16,22], [10,13,14,17,24], [18,21,23,26,30]]

        def getNum(num, data=None):
            while data:
                if num > data[0][-1]:
                    del data[0]
                    print(data)
                    getNum(num, data=None)
                elif num < data[0][-1]:
                    data = list(zip(*data))
                    del data[-1]
                    data = list(zip(*data))
                    print(data)
                    getNum(num, data=None)
                else:
                    return True
                    data.clear()
            return False


        if __name__ == '__main__':
            print(getNum(18, arr))
            
            
2. 获取最大公约数、最小公倍数

        a = 36
        b = 21

        def maxCommon(a, b):
            while b: a,b = b, a%b
            return a

        def minCommon(a, b):
            c = a*b
            while b: a,b = b, a%b
            return c//a

        if __name__ == '__main__':
            print(maxCommon(a,b))
            print(minCommon(a,b))
            
3.获取中位数

        def median(data):
            data.sort()
            half = len(data) // 2
            return (data[half] + data[~half])/2

        l = [1,3,4,53,2,46,8,42,82]

        if __name__ == '__main__':
            print(median(l))
            
4.输入一个整数，输出该数二进制表示中1的个数。其中负数用补码表示。

        def getOneCount(num):
            if num > 0:
                count = b_num.count('1')
                print(b_num)
                return count
            elif num < 0:
                b_num = bin(~num)
                count = 8 - b_num.count('1')
                return count
            else:
                return 8

        if __name__ == '__main__':
            print(getOneCount(5))
            print(getOneCount(-5))
            print(getOneCount(0))
