# HYPIR CSIG v1 第一轮训练总结

## 1. 本轮训练目标

本轮训练的目标是在官方 HYPIR `HYPIR_sd2.pth` 基础上，针对 CSIG 图像恢复比赛的数据特点进行一次定向微调。

重点希望改善：
- 真实模糊图像恢复能力
- 高频纹理和结构保真
- 减少 diffusion 过度生成和幻觉
- 为后续针对文字、小人脸、鸟羽毛、复杂树叶等区域继续优化做准备

---

## 2. 训练数据与配置

训练集：
- DIV2K 筛选后 HR 图像：400 张
- 验证集：50 张 HR 图像
- 验证集使用固定随机种子生成固定 LQ/GT 对，保证训练前后公平比较

核心训练配置：
- 基础模型：Stable Diffusion 2.1
- 初始权重：官方 `HYPIR_sd2.pth`
- 训练方式：LoRA 微调
- Batch Size：2
- Patch Size：512 × 512
- 训练步数：500 steps
- 约等于 2.5 epochs
- 每 100 step 保存一次 checkpoint
- 使用 EMA 权重进行验证
- GPU 峰值显存约 20.27 GB

训练过程中同时使用：
- HYPIR Generator
- ConvNeXt-XXLarge Discriminator
- LPIPS
- EMA

---

## 3. CSIG v1 在线退化策略

本轮训练使用在线随机退化，主要模拟比赛验证图中 case1、case2、case3、case5 的退化特征。

主要设置：
- 以各向异性模糊为主
- 不使用 Sinc 高频截断
- 不使用 USM sharpen
- 60% 保持原尺寸
- 25% 轻度下采样
- 15% 中度下采样
- 30% 概率加入轻微高斯噪声
- 50% 概率加入 JPEG 压缩
- 关闭第二阶段退化
- 不使用重度 ×4 超分退化

---

## 4. Fixed Validation 结果

官方 HYPIR baseline：

- Avg Validation Loss：`0.0144797`
- PSNR：`18.3924 dB`

Round1 checkpoint-500：

- Avg Validation Loss：`0.0111394`
- PSNR：`19.5314 dB`

变化：

- Validation Loss 下降约 23%
- PSNR 提升约 `+1.14 dB`

说明本轮训练在固定合成验证集上取得了明显的数值提升。

---

## 5. 真实 Case1~5 结果

### Official HYPIR

| Case | PSNR | SSIM |
|---|---:|---:|
| case1 | 29.3465 | 0.8464 |
| case2 | 24.2219 | 0.7314 |
| case3 | 28.9037 | 0.8123 |
| case4 | 16.3250 | 0.2570 |
| case5 | 23.8796 | 0.7773 |

### Checkpoint-500

| Case | PSNR | SSIM |
|---|---:|---:|
| case1 | 29.7171 | 0.8761 |
| case2 | 25.4001 | 0.7575 |
| case3 | 30.4804 | 0.8579 |
| case4 | 17.0429 | 0.2764 |
| case5 | 24.1106 | 0.7828 |

从指标上看，checkpoint-500 在 case1~5 的 PSNR 和 SSIM 均高于官方模型。

---

## 6. Checkpoint 趋势

从 checkpoint-100 到 checkpoint-500，整体指标基本持续改善。

较明显的提升包括：

- case2 PSNR：`24.2219 → 25.4001`
- case3 PSNR：`28.9037 → 30.4804`
- case4 PSNR：`16.3250 → 17.0429`
- case1、case5 也有稳定提升

说明当前训练并没有在 500 step 前出现明显的数值退化。

---

## 7. 当前发现的问题

虽然 PSNR、SSIM、MSE 均有改善，但实际观察中发现：

> checkpoint-500 的部分输出相比官方 HYPIR 看起来更模糊。

这说明当前训练更倾向于保守恢复：
- 减少错误高频纹理
- 降低像素误差
- 提高 PSNR / SSIM

但可能同时牺牲了一部分感知锐度。

因此，本轮结果说明：

> 模型的像素保真度提升了，但“视觉清晰度”和“感知质量”仍需要进一步优化。

后续不能只依赖 PSNR / SSIM 判断模型优劣，还需要结合：
- LPIPS
- 局部放大视觉对比
- 高频纹理恢复
- 文字、小人脸、鸟羽毛、树叶等复杂区域的真实表现

---

## 8. 当前结论

本轮 CSIG v1 微调是成功的。

训练流程已经完整跑通，包括：
- 官方 HYPIR 权重初始化
- 本地 OpenCLIP 判别器加载
- LPIPS
- 在线退化
- checkpoint 保存
- EMA 推理
- fixed validation
- 真实 case 验证

从数值结果来看，模型相较官方 HYPIR 有稳定提升。

但视觉上出现一定程度的过度平滑，因此下一阶段优化重点应从单纯追求 PSNR，转向：

> 在“保真度”和“感知清晰度”之间寻找更好的平衡。
