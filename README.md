# ComfyUI Colab Pipeline — Wan 2.2 Image-to-Video

Скрипт, който подкарва ComfyUI с Wan 2.2 видео модел на Google Colab GPU
и го прави достъпен от локален компютър през ngrok тунел.

Направих го, защото лаптопът ми няма GPU, способен да върти 14B видео модели —
а Colab има. Проблемът: ComfyUI работи на Colab машината, но интерфейсът трябва
да се отваря от моя браузър. Решението: ngrok тунел към порт 8188.

## Какво прави скриптът

1. Инсталира ComfyUI + WanVideoWrapper (custom node за Wan видео моделите)
2. Сваля Wan 2.2 моделите от Hugging Face — diffusion модели (I2V + Inpaint),
   text encoder, VAE и 4-step LoRA файлове
3. Пуска ngrok тунел и извежда публичен линк
4. Стартира ComfyUI сървъра, достъпен през линка от всяко устройство

## Как се ползва

1. Отвори скрипта в Google Colab (Runtime → смени на GPU)
2. Попълни двата токена в секция 2:
   - `token` — Hugging Face access token (huggingface.co → Settings → Access Tokens)
   - `NGROK_TOKEN` — ngrok authtoken (dashboard.ngrok.com)
3. Пусни всички клетки — първото стартиране тегли ~30+ GB модели и отнема време
4. Отвори линка от изхода — ComfyUI интерфейсът се зарежда в браузъра ти

**Никога не commit-вай токените си в Git!**

## Проблеми, които реших по пътя

- **Dependency конфликти** между ComfyUI, WanVideoWrapper и версиите на
  transformers / huggingface-hub — решени с фиксирани version ranges
- **GPU памет** — 14B моделите пълнеха VRAM-а; `PYTORCH_ALLOC_CONF=expandable_segments`
  реши фрагментацията
- **Свързаност** — Colab няма публичен IP; ngrok тунелът беше решението

## Стек

Google Colab · ComfyUI · Wan 2.2 (14B, fp8) · Hugging Face Hub · pyngrok
