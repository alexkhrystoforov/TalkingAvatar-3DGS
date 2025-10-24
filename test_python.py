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
