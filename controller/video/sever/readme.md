## 1 准备视频
对一个4k分辨率视频，生成不同分辨率的流，同时一个主M3U8文件来引用不同分辨率的流。

```bash
# 生成4K
ffmpeg -i 4k.mp4 -vf "scale=3840:2160" -c:v libx264 -b:v 8000k -hls_time 10 -hls_playlist_type vod -hls_segment_filename "4k_%03d.ts" 4k.m3u8

# 生成1080p
ffmpeg -i 4k.mp4 -vf "scale=1920:1080" -c:v libx264 -b:v 4000k -hls_time 10 -hls_playlist_type vod -hls_segment_filename "1080p_%03d.ts" 1080p.m3u8

# 生成720p
ffmpeg -i 4k.mp4 -vf "scale=1280:720" -c:v libx264 -b:v 2000k -hls_time 10 -hls_playlist_type vod -hls_segment_filename "720p_%03d.ts" 720p.m3u8

# 生成480p
ffmpeg -i 4k.mp4 -vf "scale=854:480" -c:v libx264 -b:v 1000k -hls_time 10 -hls_playlist_type vod -hls_segment_filename "480p_%03d.ts" 480p.m3u8

# 生成360p
ffmpeg -i 4k.mp4 -vf "scale=640:360" -c:v libx264 -b:v 600k -hls_time 10 -hls_playlist_type vod -hls_segment_filename "360p_%03d.ts" 360p.m3u8

```

### 1.1 创建主M3U8文件

创建一个主M3U8文件来引用不同分辨率的流。
#EXTM3U
#EXT-X-VERSION:3

# 4K流
#EXT-X-STREAM-INF:BANDWIDTH=8000000,RESOLUTION=3840x2160
4k.m3u8

# 1080p流
#EXT-X-STREAM-INF:BANDWIDTH=4000000,RESOLUTION=1920x1080
1080p.m3u8

# 720p流
#EXT-X-STREAM-INF:BANDWIDTH=2000000,RESOLUTION=1280x720
720p.m3u8

# 480p流
#EXT-X-STREAM-INF:BANDWIDTH=1000000,RESOLUTION=854x480
480p.m3u8

# 360p流
#EXT-X-STREAM-INF:BANDWIDTH=600000,RESOLUTION=640x360
360p.m3u8


保存这个文件为 `master.m3u8`。

### 1.2 部署Web服务器

将所有生成的M3U8和TS文件上传到Web服务器上。确保服务器支持HTTP范围请求，以便浏览器可以请求视频的部分内容。

## 2 配置HLS.js播放器

使用HLS.js在网页中播放自适应比特率视频流。