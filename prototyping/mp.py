import time
from multiprocessing import Process


def display(my_name):
    print ('Hi !!!' + " " + my_name)

if __name__ == '__main__':
    # target is the function we are using, the args are the input to the function
  p = Process(target=display, args=('Python',))
  p2 = Process(target=display, args=('Hello',))
  p.start()
  p2.start()
  p.join()
  p2.join()
  time.sleep(10)
  p.close()
  p2.close()