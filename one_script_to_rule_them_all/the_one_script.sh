#!/bin/bash
echo "Starting screen recording"
gnome-terminal -x /home/tmc-testi/TTY/capture_them_all/ffmpeg/ffmpeg_start_screen_and_sound_recording.sh &
echo "Starting webcam recording"
gnome-terminal -x /home/tmc-testi/TTY/capture_them_all/ffmpeg/ffmpeg_start_webcam_recording.sh &
echo "Starting keyboard and mouse capture"
gnome-terminal -x java -verbose -jar /home/tmc-testi/TTY/capture_them_all/javakeylogger/capture_them_all_runnable.jar &
