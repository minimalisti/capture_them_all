#!/bin/bash
ffmpeg -f v4l2 -video_size 1920x1080 -i /dev/video0 -vf drawtext="fontsize=24:fontfile=/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf :text='Time %{localtime} Framenumber %{frame_num}  pts %{pts \\: hms}':x=(w-text_w)-30: y=(h-text_h)-30:box=1:boxcolor=black@0.5:boxborderw=5:fontcolor=white" webcam_output`date '+%x-%X'`.mkv
