#!/bin/bash
for N in {10..5..-5}
do
   echo $N'sec'
   env sleep 5
done


TODAY=$(date +'%Y-%m-%d_%H:%M:%S')
echo $TODAY
/usr/bin/python3 /home/pi/Pieca-camera-software/camera.py --outputFolder /media/pi/8E82-4550/dcim/
