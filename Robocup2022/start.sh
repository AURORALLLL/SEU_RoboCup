#!/bin/bash
echo "开始执行move"
python /home/lynn/move.py
python /home/lynn/1.py

wait
sleep 10

# >>> conda initialize >>>
# !! Contents within this block are managed by 'conda init' !!
__conda_setup="$('/home/lynn/software/anaconda3/bin/conda' 'shell.bash' 'hook' 2> /dev/null)"
if [ $? -eq 0 ]; then
    eval "$__conda_setup"
else
    if [ -f "/home/lynn/software/anaconda3/etc/profile.d/conda.sh" ]; then
        . "/home/lynn/software/anaconda3/etc/profile.d/conda.sh"
    else
        export PATH="/home/lynn/software/anaconda3/bin:$PATH"
    fi
fi
unset __conda_setup
# <<< conda initialize <<<

echo "开始执行detect"
conda activate PyTorch
python /home/lynn/Robocup2022/light.py
python /home/lynn/Robocup2022/version4.py
python /home/lynn/faster-rcnn-pytorch-master/predict.py

exit 0



