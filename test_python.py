import torch
import cv2
import librosa
import numba
print('✅ PyTorch:', torch.__version__)
print('✅ CUDA:', torch.cuda.is_available())
print('✅ OpenCV:', cv2.__version__)
print('✅ Librosa:', librosa.__version__)
print('✅ Numba:', numba.__version__)

try:
    import edge_tts
    print('✅ edge-tts: installed')
except:
    print('❌ edge-tts: failed')

print('\n🎉 Baseline setup complete!')



import fileinput
import sys

file_path = '/usr/local/lib/python3.11/dist-packages/basicsr/data/degradations.py'
with fileinput.input(file_path, inplace=True) as f:
    for line in f:
        print(line.replace('from torchvision.transforms.functional_tensor import rgb_to_grayscale', 
                        'from torchvision.transforms.functional import rgb_to_grayscale'), end='')
