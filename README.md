
# Multi-modal Self-Instruct
[![arXiv](https://img.shields.io/badge/arXiv-Paper-b31b1b.svg)](https://github.com/zwq2018/Multi-modal-Self-instruct)
[![Project](https://img.shields.io/badge/Project-Website-blue.svg)](https://multi-modal-self-instruct.github.io)
[![HuggingFace Datasets](https://img.shields.io/badge/HuggingFace-Classic%20Smile-orange.svg)](https://huggingface.co/datasets/your_dataset_name)



The codebase for our paper: Multimodal Self-Instruct: Synthetic Abstract Image and Visual Reasoning Instruction Using Language Model

For more details, please refer to the project page with dataset exploration and visualization tools: [https://multi-modal-self-instruct.github.io](https://multi-modal-self-instruct.github.io).



## What is Multi-modal Self-Instruct?
- We identify that current LMMs have a significant gap compared to humans in understanding and visually reasoning about **abstract images**, such as maps, charts, and layouts. 

- Utilizing LLM and code, We design a multi-modal self-instruct strategy to synthesize a diverse set of abstract images and reasoning instructions, providing value data for LMMs.

- We synthesized a benchmark of 11,193 high-quality abstract images, covering eight common scenarios: **charts**, **tables**, **simulated maps**, **dashboards**, **flowcharts**, **relation graphs**, **floor plans**, and **visual puzzles**. Our benchmark exposes the shortcomings of advanced LMMs like Claude-3.5-Sonnet and GPT-4o in abstract image understanding, spatial relations reasoning, and visual element induction.

- We synthesized **62,476** chart and road map instructions for fine-tuning, verifying the effectiveness of the synthesized data.
  
![Our Benchmark](fig/figure1_final.png)


## Installation

```text
data-engine/
├── data_generator/
│ ├── algorithm
│ ├── dashboard
│ ├── iq (visual puzzles)
│ ├── flowchart
│ ├── organization (relation graph)
│ ├── utils
│ └── entry.py
├── domain_generator/
│ ├── bootstrap_domains.py
│ ├── gpt4_tools.py
│ └── filter.py
├── README.md
└── requirements.txt
```

1. Install `Graphviz` and `phantomjs` to make sure you can save images locally.
   
   - **Graphviz**: please refer to [Graphviz Download](https://graphviz.org/download/).
   - **phantomjs**: please refer to [phantomjs Download](https://phantomjs.org/download.html).

2. Install `requirements.txt`.
    ```bash
    pip install -r requirements.txt
    ```
## Abstract Image Generation
3. Domain generation.  
   Options for `type`: organization, algorithm, flowchart, dashboard.
    ```bash
    python boostrap_domains.py --type xxx
    ```
   
4. Data and plots generation.  
   Options for `type`: organization, algorithm, flowchart, dashboard.
   ```bash
    python entry.py --type xxx
    ```

5. For visual puzzles in `data_generator/iq`, run
   ```bash
    python iq.py
    ```

## Evaluation


