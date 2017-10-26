#!/bin/bash
ffmpeg -video_size 1920x1080 -f x11grab -i :0.0+0,0 -f pulse -ac 2 -i default -vf drawtext="fontsize=24:fontfile=/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf :text='Time %{localtime} Framenumber %{frame_num}  pts %{pts \\: hms}':x=(w-text_w)-30: y=(h-text_h)-30:box=1:boxcolor=black@0.5:boxborderw=5:fontcolor=white"  /home/tmc-testi/TTY/user_testing-coding-logged/latest/screen_recoding_output-`date '+%x-%X'`.mkv





