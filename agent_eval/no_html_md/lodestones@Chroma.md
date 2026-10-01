# Chroma: Open-Source, Uncensored, and Built for the Community
# use Chroma1-HD, Chroma1-Base or Chroma1-Flash instead
Chroma is a **8.9B** parameter model based on **FLUX.1-schnell** (technical report coming soon!). It’s fully **Apache 2.0 licensed**, ensuring that **anyone** can use, modify, and build on top of it—no corporate gatekeeping.
The model is **still training right now**, and I’d love to hear your thoughts! Your input and feedback are really appreciated.
* Training on a **5M dataset**, curated from **20M** samples including anime, furry, artistic stuff, and photos.
* **Fully uncensored**, reintroducing missing anatomical concepts.
* Built as a **reliable open-source option** for those who need it.
* **Hugging Face Debug Repo:** [**https://huggingface.co/lodestones/chroma-debug-development-only**](https://huggingface.co/lodestones/chroma-debug-development-only)
* **Live AIM Training Logs:** [**https://training.lodestone-rock.com**](https://training.lodestone-rock.com)
* **Training code!:** [**https://github.com/lodestone-rock/flow**](https://github.com/lodestone-rock/flow)
* **CivitAi gallery:** [**https://civitai.com/posts/13766416**](https://civitai.com/posts/13766416)
* **CivitAi model:** [**https://civitai.com/models/1330309/chroma**](https://civitai.com/models/1330309/chroma)
Shoutout to Fictional.ai for the awesome support — seriously appreciate you helping push open-source AI forward.
You can try it over on their site:
[![FictionalChromaBanner_1.png](./FictionalChromaBanner_1.png)](https://fictional.ai/?ref=chroma_hf)
The current pretraining run has already used **6000+ H100 hours**, and keeping this going long-term is expensive.
If you believe in **accessible, community-driven AI**, any support would be greatly appreciated.
👉 **[https://ko-fi.com/lodestonerock](https://ko-fi.com/lodestonerock) — Every bit helps!**
**ETH: 0x679C0C419E949d8f3515a255cE675A1c4D92A3d7**
my discord: [**discord.gg/SQVcWVbqKx**](http://discord.gg/SQVcWVbqKx)
![Chroma Workflow](./ComfyUI_Chroma1-HD_T2I-sample.png)
![Workflow Overview](./ComfyUI_Chroma1-HD_T2I-overview.png)
![Alpha_Preview](./collage.png)
- [Chroma: Open-Source, Uncensored, and Built for the Community](#chroma-open-source-uncensored-and-built-for-the-community)
- [How to run this model](#how-to-run-this-model)
  - [Architectural modifications](#architectural-modifications)
    - [12B → 8.9B](#12b-%E2%86%92-89b)
    - [MMDiT masking](#mmdit-masking)
    - [Timestep Distributions](#timestep-distributions)
    - [Minibatch Optimal Transport](#minibatch-optimal-transport) [WIP]
    - [Prior preserving distribution training] [WIP]
    - [blockwise droppout optimizers] [WIP]
- [Chroma checkpoint](https://huggingface.co/lodestones/Chroma) (pick the latest version on this repo)
- [Alternative option: FP8 Scaled Quant](https://huggingface.co/Clybius/Chroma-fp8-scaled) (Format used by ComfyUI with possible inference speed increase)
- [Alternative option: GGUF Quantized](https://huggingface.co/silveroxides/Chroma-GGUF) (You will need to install ComfyUI-GGUF custom node)
- [T5 XXL](https://huggingface.co/comfyanonymous/flux_text_encoders/resolve/main/t5xxl_fp16.safetensors) or [T5 XXL fp8](https://huggingface.co/comfyanonymous/flux_text_encoders/resolve/main/t5xxl_fp8_e4m3fn.safetensors) (either of them will work)
- [FLUX VAE](https://huggingface.co/lodestones/Chroma/resolve/main/ae.safetensors)
- [Chroma_Workflow](https://huggingface.co/lodestones/Chroma/resolve/main/ComfyUI_Chroma1-HD_T2I-workflow.json)
###  Deprecated: Manual Installation (Chroma)
1. Navigate to your ComfyUI's `ComfyUI/custom_nodes` folder
git clone https://github.com/lodestone-rock/ComfyUI_FluxMod.git
4. Refresh your browser if ComfyUI is already running
1. put `T5_xxl` into `ComfyUI/models/clip` folder
2. put `FLUX VAE` into `ComfyUI/models/vae` folder
3. put `Chroma checkpoint` into `ComfyUI/models/diffusion_models` folder
4. load chroma workflow to your ComfyUI
### TL;DR: There are 3.3B parameters that only encode a single input vector, which I replaced with 250M params.
Since FLUX is so big, I had to modify the architecture and ensure minimal knowledge was lost in the process. The most obvious thing to prune was this modulation layer. In the diagram, it may look small, but in total, FLUX has 3.3B parameters allocated to it. Without glazing over the details too much, this layer's job is to let the model know which timestep it's at during the denoising process. This layer also receives information from pooled CLIP vectors.
![affine_projection_AdaLN_begone](./prune.png)
But after a simple experiment of zeroing these pooled vectors out, the model’s output barely changed—which made pruning a breeze! Why? Because the only information left for this layer to encode is just a single number in the range of 0-1.
Yes, you heard it right—3.3B parameters were used to encode 8 bytes of float values. So this was the most obvious layer to prune and replace with a simple FFN. The whole replacement process only took a day on my single 3090, and after that, the model size was reduced to just 8.9B.
### TL;DR: Masking T5 padding tokens enhanced fidelity and increased stability during training.
It might not be obvious, but BFL had some oversight during pre-training where they forgot to mask both T5 and MMDiT tokens. So, for example, a short sentence like “a cat sat on a mat” actually looks like this in both T5 and MMDiT:
The model ends up paying way too much attention to padding tokens, drowning out the actual prompt information. The fix? Masking—so the model doesn’t associate anything with padding tokens.
But there’s a catch: if you mask out all padding tokens, the model falls out of distribution and generates a blurry mess. The solution? Unmask just one padding token while masking the rest.
With this fix, MMDiT now only needs to pay attention to:
### TL;DR: A custom timestep distribution prevents loss spikes during training.
When training a diffusion/flow model, we sample random timesteps—but not evenly. Why? Because empirically, training on certain timesteps more often makes the model converge faster.
FLUX uses a "lognorm" distribution, which prioritizes training around the middle timesteps. But this approach has a flaw: the tails—where high-noise and low-noise regions exist—are trained super sparsely.
If you train for a looong time (say, 1000 steps), the likelihood of hitting those tail regions is almost zero. The problem? When the model finally does see them, the loss spikes hard, throwing training out of whack—even with a huge batch size.
The fix is simple: sample and train those tail timesteps a bit more frequently using a `-x^2` function instead. You can see in the image that this makes the distribution thicker near 0 and 1, ensuring better coverage.
## Minibatch Optimal Transport
### TL;DR: Transport problem math magic :P
This one’s a bit math-heavy, but here’s the gist: FLUX isn’t actually "denoising" an image. What we’re really doing is training a vector field to map one distribution (noise) to another (image). Once the vector field is learned, we "flow" through it to transform noise into an image.
To keep it simple—just check out these two visuals:
By choosing better pairing through math magic it accelerates training by reducing the “path ambiguity” 
  title = {{Chroma: Open-Source, Uncensored, and Built for the Community}},
  note = {Hugging Face repository},
  howpublished = {\url{https://huggingface.co/lodestones/Chroma}},