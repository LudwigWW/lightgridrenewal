import socket
import struct
import time
import numpy as np
import cv2
import random
import os

serial_connected = 0
if os.path.exists('/dev/ttyACM0') == True:
    import serial
    ser = serial.Serial('/dev/ttyACM0', 115200)
    serial_connected = 1
    time.sleep(1)

#gamma correction
gamma = np.array([0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
    0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1,  1,  1,  1,
    1,  1,  1,  1,  1,  1,  1,  1,  1,  2,  2,  2,  2,  2,  2,  2,
    2,  3,  3,  3,  3,  3,  3,  3,  4,  4,  4,  4,  4,  5,  5,  5,
    5,  6,  6,  6,  6,  7,  7,  7,  7,  8,  8,  8,  9,  9,  9, 10,
   10, 10, 11, 11, 11, 12, 12, 13, 13, 13, 14, 14, 15, 15, 16, 16,
   17, 17, 18, 18, 19, 19, 20, 20, 21, 21, 22, 22, 23, 24, 24, 25,
   25, 26, 27, 27, 28, 29, 29, 30, 31, 32, 32, 33, 34, 35, 35, 36,
   37, 38, 39, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 50,
   51, 52, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 66, 67, 68,
   69, 70, 72, 73, 74, 75, 77, 78, 79, 81, 82, 83, 85, 86, 87, 89,
   90, 92, 93, 95, 96, 98, 99,101,102,104,105,107,109,110,112,114,
  115,117,119,120,122,124,126,127,129,131,133,135,137,138,140,142,
  144,146,148,150,152,154,156,158,160,162,164,167,169,171,173,175,
  177,180,182,184,186,189,191,193,196,198,200,203,205,208,210,213,
  215,218,220,223,225,228,231,233,236,239,241,244,247,249,252,255])

#this sets up network things
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = '4.3.2.1'
server_port = 21324
server = (server_address, server_port)
#this is the protocol # for the dnrgb protocol
DNRGB_PROTOCOL_VALUE = 4


#this function takes an input between 0 and 2.8, and outputs a value between 0 and 1, with 1 being 2.8V and 0 being 0.05V
def voltage_to_value(voltage):
    if voltage > 2.8:
        voltage = 2.8
    if voltage < 0.05:
        voltage = 0.05
    return (voltage - 0.05) / 2.75

def get_knob_value():
    return 0
    for x in range (0,1):
        command = str(x) + "\n"
        ser.write(bytes(command.encode('ascii')))
        if ser.inWaiting() > 0:
            pico_data = ser.readline()
            pico_data = pico_data.decode("utf-8","ignore")
            string = pico_data[:-2]
            #print (string[string.find(':')+6:])
            try:
                print("[]")
                return( voltage_to_value ( ((int(string[string.find(':')+6:]))* (3.3/65535))))
            except:
                print("failed")
                pass


def sp_noise(image,prob):
    '''
    Add salt and pepper noise to image
    prob: Probability of the noise
    '''
    output = np.zeros(image.shape,np.uint8)
    thres = 1 - prob 
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            rdn = random.random()
            if rdn < prob:
                output[i][j] = 0
            elif rdn > thres:
                output[i][j] = 255
            else:
                output[i][j] = image[i][j]
    return output


#this function creates the header for the dnrgb protocol
def dnrgb_header(wait_time: int, start_index: int) -> bytes:
    if wait_time > 255:
        raise ValueError("Wait time must be within 0-255")
    if start_index > 2**16 - 1:
        raise ValueError("Start index must be a nonnegative 16-bit number")
    return struct.pack(">BBH", DNRGB_PROTOCOL_VALUE, wait_time, start_index)

#this function sends the rgb values to the server
def send_rgb(rgb_values, start_index=0):
    byte_string = dnrgb_header(5, start_index) + bytes(rgb_values)
    #print("Header + Package",byte_string)

    sent = sock.sendto(byte_string, server)
    #print("Sent " + str(sent) + " bytes to " + str(server))
    return

#this padds the list of RGB values so the total length of the list is 1467
def function_padder(rgb_values):
    rgb_values = rgb_values + [50] * (1467 - len(rgb_values))
    return rgb_values


def start_cam(x,y):
    # Start the webcam
    webcam = cv2.VideoCapture(0)

    # Set frame rate to 45 frames per second
    frame_rate = 45

    # Loop 45 times per second
    frame_count = 0
    #start counting time
    start_time = time.time()
    while True:
        #if framecount is 60, set it to 0 and print the time it took
        frame_count += 1
        if frame_count == 60:
            frame_count = 0
            print("frame time for 60:",time.time() - start_time)
            start_time = time.time()
        # Capture a frame from the webcam
        ret, frame = webcam.read()

        # Resize the frame to 16x16
        frame = cv2.LUT(cv2.resize(frame, (x, y)), gamma)

        #apply SP_Noise effect
        frame = sp_noise(frame, get_knob_value())

        #apply desaturation effect
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
        frame[:,1,:] = frame[:,1,:] * 0
        frame = cv2.cvtColor(frame, cv2.COLOR_HSV2BGR)

        # Get input orientation
        orientation = 0
        # Rotate the frame by 90 degrees based on user input
        if orientation == 1:
            frame = np.rot90(frame)
        elif orientation == 2:
            frame = np.rot90(frame, 2)
        elif orientation == 3:
            frame = np.rot90(frame, 3)

        #flatten frame using numpy
        frame = frame.flatten()

        #rgb_out = average_pixels(rgb_out)
        temp_send(frame, x,y)

#this function takes an input array of rgb values, and the dimensions of the array, and splits it into 4 equal arrays, then padds them to ensure they fit the packet length
def split_rgb(rgb_values, x, y):
    rgb_values1 = rgb_values[0:(3*x*y)//4]
    rgb_values2 = rgb_values[(3*x*y)//4:(3*x*y)//2]
    rgb_values3 = rgb_values[(3*x*y)//2:(3*3*x*y)//4]
    rgb_values4 = rgb_values[(3*3*x*y)//4:(3*x*y)]
    return rgb_values1, rgb_values2, rgb_values3, rgb_values4



#temp sending function
def temp_send(rgb_values, x, y):
    rgb_values1, rgb_values2, rgb_values3, rgb_values4 = split_rgb(rgb_values, 32, 32)
    send_rgb(rgb_values1, 0)
    send_rgb(rgb_values2, (x*y)//4)
    send_rgb(rgb_values3, (x*y)//2)
    send_rgb(rgb_values4, (3*x*y)//4)



start_cam(32,32)
