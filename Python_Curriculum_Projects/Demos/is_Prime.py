#求区间内质数
def is_prime(number):
    if number in (1, 2):
        return True
    for idx in range(3,number) :
        if number % idx == 0:
            return False
    return True

def print_prime(begin, end) :
    for number in range(begin, end+1) :
        if is_prime(number):
            print(f"{number} is a prime")


begin = eval(input())
end = eval(input())
print_prime(begin, end)
