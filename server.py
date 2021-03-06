import pyaudio
import socket
from threading import Thread

frames = []

def udpStream(CHUNK):

    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp.bind(("10.0.0.6", 12121))

    while True:
        soundData, addr = udp.recvfrom(CHUNK * CHANNELS * 4)
        frames.append(soundData)

    udp.close()

def play(stream, CHUNK):
    BUFFER = 10
    while True:
        if len(frames) > BUFFER:
            #while frames[1]:
            #print("bool mr over : ", len(frames) )
            #stream.write(frames.pop(0))
            stream.write(frames[0])
            frames.pop(0)
                  

if __name__ == "__main__":
    FORMAT = pyaudio.paInt16
    CHUNK = 1024
    CHANNELS = 1
    RATE = 4000

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels = CHANNELS,
                    rate = RATE,
                    output = True,
                    frames_per_buffer = CHUNK,
                    )

    Ts = Thread(target = udpStream, args=(CHUNK,))
    Tp = Thread(target = play, args=(stream, CHUNK,))
    Ts.setDaemon(True)
    Tp.setDaemon(True)
    Ts.start()
    Tp.start()
    Ts.join()
    Tp.join()
