from pyspark import SparkConf, SparkContext

if __name__ == '__main__':
    conf = SparkConf().setAppName("test").setMaster('local[*]')

    sc = SparkContext(conf=conf)
    # 读取本地文件系统
    file_rdd1 = sc.textFile('/demo/Data01.txt')
    print("默认读取分区数", file_rdd1.getNumPartitions())
    print("file_rdd1内容:", file_rdd1.collect())

    file_rdd2 = sc.textFile('/demo/Data01.txt', 3)
    file_rdd3 = sc.textFile('/demo/Data01.txt', 100)

    print("rdd2分区数", file_rdd2.getNumPartitions())
    print("rdd3分区数", file_rdd3.getNumPartitions())


    hdfs_rdd = sc.textFile("hdfs://node01:8020/input/words.txt")
    print("hdfs_rdd内容", hdfs_rdd.collect())

