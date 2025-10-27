#蒙特卡洛求pi
import random
def monte_carlo(sample_num):
    points_inside = 0
    for i in range(sample_num):
        x = random.random()
        y = random.random()
        if x**2 + y**2 <= 1:
            points_inside += 1

    return 4 * points_inside / sample_num


sample_num = int(1e5)
print(monte_carlo(sample_num))
