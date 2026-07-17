# --- 1. ПРЕДВАРИТЕЛНА ИНСТАЛАЦИЯ ---
!pip install pyngrok --quiet
import os
from pyngrok import ngrok
# --- 2. ПАРАМЕТРИ ---
token = ""        # <-- сложи своя Hugging Face token тук
NGROK_TOKEN = ""  # <-- сложи своя ngrok token тук
# --- 3. ИНСТАЛАЦИЯ НА COMFYUI И WRAPPER ---
if not os.path.exists('/content/ComfyUI'):
    print("🚀 Първоначална инсталация на ComfyUI и WanVideoWrapper...")
    %cd /content
    !git clone https://github.com/comfyanonymous/ComfyUI
    %cd ComfyUI
    !git clone https://github.com/kijai/ComfyUI-WanVideoWrapper custom_nodes/ComfyUI-WanVideoWrapper
    !pip install -r requirements.txt
    !pip install -r custom_nodes/ComfyUI-WanVideoWrapper/requirements.txt
    !pip install "huggingface-hub[cli]>=0.24.0,<1.0" "transformers>=4.48.0" onnxruntime-gpu --upgrade
# --- 4. ТЕГЛЕНЕ НА ВСИЧКИ WAN 2.2 МОДЕЛИ (I2V + INPAINT) ---
print("📦 Проверка и теглене на моделите (това може да отнеме време)...")
# Списък с файлове за теглене
models = [
    # Text Encoder & VAE
    ("Comfy-Org/Wan_2.1_ComfyUI_repackaged", "split_files/text_encoders/umt5_xxl_fp8_e4m3fn_scaled.safetensors", "models/text_encoders"),
    ("Comfy-Org/Wan_2.2_ComfyUI_Repackaged", "split_files/vae/wan_2.1_vae.safetensors", "models/vae"),
    
    # Diffusion Models (I2V Standard)
    ("Comfy-Org/Wan_2.2_ComfyUI_Repackaged", "split_files/diffusion_models/wan2.2_i2v_high_noise_14B_fp8_scaled.safetensors", "models/diffusion_models"),
    ("Comfy-Org/Wan_2.2_ComfyUI_Repackaged", "split_files/diffusion_models/wan2.2_i2v_low_noise_14B_fp8_scaled.safetensors", "models/diffusion_models"),
    
    # Diffusion Models (Inpaint - НОВО)
    ("Comfy-Org/Wan_2.2_ComfyUI_Repackaged", "split_files/diffusion_models/wan2.2_fun_inpaint_high_noise_14B_fp8_scaled.safetensors", "models/diffusion_models"),
    ("Comfy-Org/Wan_2.2_ComfyUI_Repackaged", "split_files/diffusion_models/wan2.2_fun_inpaint_low_noise_14B_fp8_scaled.safetensors", "models/diffusion_models"),
    
    # LoRAs (4-Steps)
    ("Comfy-Org/Wan_2.2_ComfyUI_Repackaged", "split_files/loras/wan2.2_i2v_lightx2v_4steps_lora_v1_high_noise.safetensors", "models/loras"),
    ("Comfy-Org/Wan_2.2_ComfyUI_Repackaged", "split_files/loras/wan2.2_i2v_lightx2v_4steps_lora_v1_low_noise.safetensors", "models/loras")
]
for repo, file, target_dir in models:
    !huggingface-cli download {repo} {file} --local-dir /content/ComfyUI/{target_dir} --local-dir-use-symlinks False --token {token}
# --- 5. СТАРТ НА NGROK ТУНЕЛ ---
ngrok.kill() # Затваряме всичко старо за всеки случай
ngrok.set_auth_token(NGROK_TOKEN)
try:
    url = ngrok.connect(8188)
    print(f"\n🌍 ТВОЯТ ЛИНК: {url}\n")
except Exception as e:
    print(f"Ngrok error: {e}")
# --- 6. СТАРТ НА COMFYUI ---
os.environ['PYTORCH_ALLOC_CONF'] = "expandable_segments:True"
%cd /content/ComfyUI
!python main.py --dont-print-server --listen 0.0.0.0