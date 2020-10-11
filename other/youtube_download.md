# youtube download


## install youtube-dl

    pip3 install --upgrade youtube-dl


## example

    export HTTP_PROXY=http://127.0.0.1:8888
    export HTTPS_PROXY=http://127.0.0.1:8888
    export http_proxy=http://127.0.0.1:8888
    export https_proxy=http://127.0.0.1:8888
    youtube-dl -f 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best' 'https://www.youtube.com/watch?v=Sjwl23rk6Tg&ab_channel=Cocomelon-NurseryRhymes'

## 说明

    若是1080P的，音频视频是分离的，需用ffmpeg合并
    1. 安装仓库
        sudo dnf -y install https://download1.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E %fedora).noarch.rpm
        sudo dnf -y install https://download1.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-$(rpm -E %fedora).noarch.rpm
    2. 安装
        sudo dnf -y install ffmpeg
    3. 合并视频
        ffmpeg -i audio.mp4 -i video.mp4 -acodec copy -vcodec copy output.mp4
