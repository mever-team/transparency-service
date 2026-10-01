![magi-logo](figures/logo_black.png)
# MAGI-1: Autoregressive Video Generation at Scale
This repository contains the [code](https://github.com/SandAI-org/MAGI-1) for the MAGI-1 model, pre-trained weights and inference code. You can find more information on our [technical report](https://static.magi.world/static/files/MAGI_1.pdf) or directly create magic with MAGI-1 [here](http://sand.ai) . 🚀✨
- May 30, 2025: Support for ComfyUI is added 🎉 — the custom nodes for MAGI-1 are now available. Try them out in your workflows!
- May 26, 2025: MAGI-1 4.5B distill and distill+quant models has been released 🎉 — we’ve updated the model weights - check it out!
- May 14, 2025: Added Dify DSL for prompt enhancement 🎉 — import it into Dify to boost prompt quality!
- Apr 30, 2025: MAGI-1 4.5B model has been released 🎉. We've updated the model weights — check it out!
- Apr 21, 2025: MAGI-1 is here 🎉. We've released the model weights and inference code — check it out!
We present MAGI-1, a world model that generates videos by ***autoregressively*** predicting a sequence of video chunks, defined as fixed-length segments of consecutive frames. Trained to denoise per-chunk noise that increases monotonically over time, MAGI-1 enables causal temporal modeling and naturally supports streaming generation. It achieves strong performance on image-to-video (I2V) tasks conditioned on text instructions, providing high temporal consistency and scalability, which are made possible by several algorithmic innovations and a dedicated infrastructure stack. MAGI-1 further supports controllable generation via chunk-wise prompting, enabling smooth scene transitions, long-horizon synthesis, and fine-grained text-driven control. We believe MAGI-1 offers a promising direction for unifying high-fidelity video generation with flexible instruction control and real-time deployment.
- Variational autoencoder (VAE) with transformer-based architecture, 8x spatial and 4x temporal compression.
- Fastest average decoding time and highly competitive reconstruction quality
### Auto-Regressive Denoising Algorithm
MAGI-1 is an autoregressive denoising video generation model generating videos chunk-by-chunk instead of as a whole. Each chunk (24 frames) is denoised holistically, and the generation of the next chunk begins as soon as the current one reaches a certain level of denoising. This pipeline design enables concurrent processing of up to four chunks for efficient video generation.
![auto-regressive denosing algorithm](figures/algorithm.png)
### Diffusion Model Architecture
MAGI-1 is built upon the Diffusion Transformer, incorporating several key innovations to enhance training efficiency and stability at scale. These advancements include Block-Causal Attention, Parallel Attention Block, QK-Norm and GQA, Sandwich Normalization in FFN, SwiGLU, and Softcap Modulation. For more details, please refer to the [technical report.](https://static.magi.world/static/files/MAGI_1.pdf)
We adopt a shortcut distillation approach that trains a single velocity-based model to support variable inference budgets. By enforcing a self-consistency constraint—equating one large step with two smaller steps—the model learns to approximate flow-matching trajectories across multiple step sizes. During training, step sizes are cyclically sampled from {64, 32, 16, 8}, and classifier-free guidance distillation is incorporated to preserve conditional alignment. This enables efficient inference with minimal loss in fidelity.
We provide the pre-trained weights for MAGI-1, including the 24B and 4.5B models, as well as the corresponding distill and distill+quant models. The model weight links are shown in the table.
> For 4.5B models, any machine with at least 24GB of GPU memory is sufficient.
MAGI-1 achieves state-of-the-art performance among open-source models like Wan-2.1 and HunyuanVideo and closed-source model like Hailuo (i2v-01), particularly excelling in instruction following and motion quality, positioning it as a strong potential competitor to closed-source commercial models such as Kling.
![inhouse human evaluation](figures/inhouse_human_evaluation.png)
Thanks to the natural advantages of autoregressive architecture, Magi achieves far superior precision in predicting physical behavior on the [Physics-IQ benchmark](https://github.com/google-deepmind/physics-IQ-benchmark) through video continuation—significantly outperforming all existing models.
We provide two ways to run MAGI-1, with the Docker environment being the recommended option.
**Run with Docker Environment (Recommend)**
docker pull sandai/magi:latest
docker run -it --gpus all --privileged --shm-size=32g --name magi --net=host --ipc=host --ulimit memlock=-1 --ulimit stack=6710886 sandai/magi:latest /bin/bash
conda create -n magi python==3.10.12
conda install pytorch==2.4.0 torchvision==0.19.0 torchaudio==2.4.0 pytorch-cuda=12.4 -c pytorch -c nvidia
pip install -r requirements.txt
conda install -c conda-forge ffmpeg=4.4
# For GPUs based on the Hopper architecture (e.g., H100/H800), it is recommended to install MagiAttention(https://github.com/SandAI-org/MagiAttention) for acceleration. For non-Hopper GPUs, installing MagiAttention is not necessary.
git clone git@github.com:SandAI-org/MagiAttention.git
git submodule update --init --recursive
pip install --no-build-isolation .
To run the `MagiPipeline`, you can control the input and output by modifying the parameters in the `example/24B/run.sh` or `example/4.5B/run.sh` script. Below is an explanation of the key parameters:
- `--config_file`: Specifies the path to the configuration file, which contains model configuration parameters, e.g., `example/24B/24B_config.json`.
- `--mode`: Specifies the mode of operation. Available options are:
- `--prompt`: The text prompt used for video generation, e.g., `"Good Boy"`.
- `--image_path`: Path to the image file, used only in `i2v` mode.
- `--prefix_video_path`: Path to the prefix video file, used only in `v2v` mode.
- `--output_path`: Path where the generated video file will be saved.
You can modify the parameters in `run.sh` as needed. For example:
- To use the Image to Video mode (`i2v`), set `--mode` to `i2v` and provide `--image_path`:
  --image_path example/assets/image.jpeg \
- To use the Video to Video mode (`v2v`), set `--mode` to `v2v` and provide `--prefix_video_path`:
  --prefix_video_path example/assets/prefix_video.mp4 \
By adjusting these parameters, you can flexibly control the input and output to meet different requirements.
### Some Useful Configs (for config.json)
> - If you are running 24B model with RTX 4090 \* 8, please set `pp_size:2 cp_size: 4`.
> - Our model supports arbitrary resolutions. To accelerate inference process, the default resolution for the 4.5B model is set to 720×720 in the `4.5B_config.json`.
This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.
If you find our code or model useful in your research, please cite:
@misc{ai2025magi1autoregressivevideogeneration,
      title={MAGI-1: Autoregressive Video Generation at Scale},
      author={Sand. ai and Hansi Teng and Hongyu Jia and Lei Sun and Lingzhi Li and Maolin Li and Mingqiu Tang and Shuai Han and Tianning Zhang and W. Q. Zhang and Weifeng Luo and Xiaoyang Kang and Yuchen Sun and Yue Cao and Yunpeng Huang and Yutong Lin and Yuxin Fang and Zewei Tao and Zheng Zhang and Zhongshu Wang and Zixun Liu and Dai Shi and Guoli Su and Hanwen Sun and Hong Pan and Jie Wang and Jiexin Sheng and Min Cui and Min Hu and Ming Yan and Shucheng Yin and Siran Zhang and Tingting Liu and Xianping Yin and Xiaoyu Yang and Xin Song and Xuan Hu and Yankai Zhang and Yuqiao Li},
      url={https://arxiv.org/abs/2505.13211},
If you have any questions, please feel free to raise an issue or contact us at [research@sand.ai](mailto:research@sand.ai) .