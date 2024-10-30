# codeing:utf8

from pyspark import SparkConf,SparkContext

if __name__ == '__main__':
    conf = SparkConf().setAppName("WordCountHelloWorld")
    sc = SparkContext(conf=conf)

    # Word Count单词计数
    # 读取文件
    file_rdd = sc.textFile("hdfs://node01:8020/input/words.txt")

    # 切割单词
    words_rdd = file_rdd.flatMap(lambda line : line.split(" "))

    # 将单词转化为元组对象
    words_with_one_rdd = words_rdd.map(lambda x : (x,1))

    # 将元组的值按照键分组, 对所有的值执行聚合操作
    result_rdd = words_with_one_rdd.reduceByKey(lambda a, b :a+b)

    # 收集返回值, 输出结果
    print(result_rdd.collect())
