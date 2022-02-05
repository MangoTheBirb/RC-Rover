# This is the pythton code for controlling the car. Currently I just have it working over wifi. Using cell data is the next step.
# I have used other people's code for aspects of this. I will add credits soon.
# It isn't fully working right now. I mostly wanted to test the socket streaming server, so the car controls aren't working.

import pigpio
import time
import pygame
from pygame.locals import *
import io
import picamera
import logging
import socketserver
from threading import Condition
from http import server

pygame.init()
screen = pygame.display.set_mode((240, 240))
pygame.display.set_caption('Wifi-Rustler')

pi = pigpio.pi()

servoPIN = 18
escPIN = 19

throt_pwm = 1500
steer_pwm = 1500

default_throt_pwm = 1500
default_steer_pwm = 1500

pi.set_mode(servoPIN, pigpio.OUTPUT)
pi.set_mode(escPIN, pigpio.OUTPUT)

PAGE="""\
<html>
<head>
<title>Wifi-Rustler</title>
</head>
<body>
<center><h1>Wifi-Rustler</h1></center>
<center><img src="stream.mjpg" width="640" height="480"></center>
</body>
</html>
"""

class StreamingOutput(object):
    def __init__(self):
        self.frame = None
        self.buffer = io.BytesIO()
        self.condition = Condition()

    def write(self, buf):
        if buf.startswith(b'\xff\xd8'):
            # New frame, copy the existing buffer's content and notify all
            # clients it's available
            self.buffer.truncate()
            with self.condition:
                self.frame = self.buffer.getvalue()
                self.condition.notify_all()
            self.buffer.seek(0)
        return self.buffer.write(buf)

class StreamingHandler(server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(301)
            self.send_header('Location', '/index.html')
            self.end_headers()
        elif self.path == '/index.html':
            content = PAGE.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        elif self.path == '/stream.mjpg':
            self.send_response(200)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers()
            try:
                while True:
                    with output.condition:
                        output.condition.wait()
                        frame = output.frame
                    self.wfile.write(b'--FRAME\r\n')
                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Content-Length', len(frame))
                    self.end_headers()
                    self.wfile.write(frame)
                    self.wfile.write(b'\r\n')
            except Exception as e:
                logging.warning(
                    'Removed streaming client %s: %s',
                    self.client_address, str(e))
        else:
            self.send_error(404)
            self.end_headers()

class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True

with picamera.PiCamera(resolution='640x480', framerate=24) as camera:
    output = StreamingOutput()
    #Uncomment the next line to change your Pi's Camera rotation (in degrees)
    #camera.rotation = 90
    camera.start_recording(output, format='mjpeg')
    try:
        address = ('', 8000)
        server = StreamingServer(address, StreamingHandler)
        server.serve_forever()
    finally:
        camera.stop_recording()

stop = False
while stop != True:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == K_w:
                throt_pwm = 1650
            elif event.key == K_s:
                throt_pwm = 1350
            elif event.key == K_a:
                steer_pwm = 2200
            elif event.key == K_d:
                steer_pwm = 800
            elif event.key == K_ESCAPE:
                stop = True
            pi.set_servo_pulsewidth(escPIN, throt_pwm)
            pi.set_servo_pulsewidth(servoPIN, steer_pwm)
        elif event.type == pygame.KEYUP:
            if((pygame.key.get_pressed()[pygame.K_w] != 0 and pygame.key.get_pressed()[pygame.K_a] == 0) or (pygame.key.get_pressed()[pygame.K_w] !=0 and pygame.key.get_pressed()[pygame.K_d] == 0)):
                steer_pwm = default_steer_pwm
                throt_pwm = throt_pwm
            elif((pygame.key.get_pressed()[pygame.K_s] != 0 and pygame.key.get_pressed()[pygame.K_a] == 0) or (pygame.key.get_pressed()[pygame.K_s] !=0 and pygame.key.get_pressed()[pygame.K_d] == 0)):
                steer_pwm = default_steer_pwm
                throt_pwm = throt_pwm
            elif((pygame.key.get_pressed()[pygame.K_s] == 0 and pygame.key.get_pressed()[pygame.K_a] != 0) or (pygame.key.get_pressed()[pygame.K_s] ==0 and pygame.key.get_pressed()[pygame.K_d] != 0)):
                steer_pwm = steer_pwm
                throt_pwm = default_throt_pwm
            elif((pygame.key.get_pressed()[pygame.K_w] == 0 and pygame.key.get_pressed()[pygame.K_a] != 0) or (pygame.key.get_pressed()[pygame.K_w] ==0 and pygame.key.get_pressed()[pygame.K_d] != 0)):
                steer_pwm = steer_pwm
                throt_pwm = default_throt_pwm
            elif(pygame.key.get_pressed()[pygame.K_w] != 0):
                throt_pwm = default_throt_pwm
            elif(pygame.key.get_pressed()[pygame.K_s] != 0):
                throt_pwm = default_throt_pwm
            elif(pygame.key.get_pressed()[pygame.K_a] != 0):
                steer_pwm = default_steer_pwm
            elif(pygame.key.get_pressed()[pygame.K_d] != 0):
                steer_pwm = default_steer_pwm
            else:
                steer_pwm = default_steer_pwm
                throt_pwm = default_throt_pwm
            pi.set_servo_pulsewidth(escPIN, throt_pwm)
            pi.set_servo_pulsewidth(servoPIN, steer_pwm)
pi.stop()
