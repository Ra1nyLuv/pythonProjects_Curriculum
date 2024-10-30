from pyspark import SparkConf,SparkContext

if __name__ == '__main__':
    # 初始化执行环境, 构建SparkContext对象
    conf = SparkConf().setAppName('test').setMaster('local[*]')
    sc = SparkContext(conf=conf)

    # 通过并行化集合的方式创建RDD
    rdd = sc.parallelize([1,2,3,4,5,6,7,8,9])
    # parallelize方法, 没有给定分区数, 默认分区数根据CPU核心确定
    print("默认分区数:", rdd.getNumPartitions())

    rdd = sc.parallelize([1,2,3], 3)
    print("分区数", rdd.getNumPartitions())
    # collect方法, 是将RDD中每个分区的数据, 都发送到Driver中, 形成一个List对象
    print("rdd的内容:", rdd.collect())

