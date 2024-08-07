import time

def mixpenhere(times,a,b) :
    start_time = time.time()
    for i in range(times) :
        print(i)
        print("i neem i sus")
        print(a+b)
    end_time = time.time()
    print(end_time-start_time)

mixpenhere(100000,123465,741852)