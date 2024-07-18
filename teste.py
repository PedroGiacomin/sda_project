import threading as th

timer = th.Timer(5000.0, print('deu'))
while True:
    timer.start()