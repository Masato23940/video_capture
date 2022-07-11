ffmpeg \
-stream_loop -1 -i Music/no_sound.mp3 \
-f v4l2 -s 640x480 -r 20 -i /dev/video0 \
-vcodec libx264 \
-vf drawtext="fontfile=/usr/share/fonts/truetype/noto/NotoMono-Regular.ttf:x=2:y=2:fontsize=32:fontcolor=white:box=1:boxcolor=black@0.4:text='%{localtime}'" \
-pix_fmt yuv420p -preset ultrafast -r 20 -g 30 -b:v 500k \
-acodec aac -ar 44100 -threads 2 -b:a 128k -bufsize 512k \
-f flv rtmp://a.rtmp.youtube.com/live2/6b2u-eq6x-3w26-twy7-8pu2

# -i:read file command
# -stream_loop:loop endless option 

# -f:Specifying the conversion format (passed from the camera modul) (option)
# -s:image size, -r:frame rate for capture (option)
# -i:reading camera image

# -vcodec:Specify video codec (option)
# -vf:Specify the effect draw text (option)
# -preset:encode speed (option)
# -r:Output video frame rate, -g:GOP size=30fpsx2s, -b:v:output video bitrate (option)

# -acodec:output sound codec (option)
# -ar:output sound sampling rate, -threads:Number of threads for encoding
# -b:a:output sound bitrate, -bufsize:buffer size

#-f:output video format flv, rtmp:output destinationK
