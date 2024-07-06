
# Self-Instruct Data Engine

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

## Installation

1. Install `Graphviz` and `phantomjs` to make sure you can save images locally.
   
   - **Graphviz**: please refer to [Graphviz Download](https://graphviz.org/download/).
   - **phantomjs**: please refer to [phantomjs Download](https://phantomjs.org/download.html).

2. Install `requirements.txt`.
    ```bash
    pip install -r requirements.txt
    ```
## Data Generation
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

## Our benchmark Evaluation


