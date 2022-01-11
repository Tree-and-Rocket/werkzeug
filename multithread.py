from multiprocessing import Pool, cpu_count


def myFunction(func, data):
    p = Pool(cpu_count())
    p.map(func, data)



