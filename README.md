<p align="center">
    <img src="data/images/logo.png" alt="logo" width=600>
</p>


**Multi-Agent MT** is a pipeline-based AI agent framework that progressively refines translations via **Translate → Post-edit → Proofread**.


# 🗞️ News
- **Dec 27, 2025** — Version 1.0 officially released
- **Nov 8, 2025** — Our work was accepted and presented at the Conference on Machine Translation (WMT) 2025

# ✺ Features
- Support for both single-task and multi-task execution modes  
- Integration of [Rubric-MQM](https://github.com/trotacodigos/Rubric-MQM) as an automatic post-editing (APE) component  
- Fully asynchronous OpenAI API integration   

# ✺  Quick Start
### ➡ Set your OpenAI API key
```bash
export OPENAI_API_KEY=sk-xxxx
# or
export OPENAI_API_KEYS=sk-key1,sk-key2
```

### ➡ Clone Rubric-MQM as a submodule
This project uses Rubric-MQM as an automatic post-editing (APE) component.
Clone it under the name rubric_mqm and add it to PYTHONPATH.

```bash
git clone https://github.com/trotacodigos/Rubric-MQM rubric_mqm
export PYTHONPATH=$PYTHONPATH:/your/full/path/to/rubric_mqm
```

### ➡ Configuration (YAML)
You can run the system in either single-task mode (one agent) or multi-task mode (full pipeline: translate → postedit → proofread).
Model selection and decoding parameters are fully configurable via YAML.

🤖 **Single-tasker Example** [(config file ↗)](config/single.yaml)
```yaml
task: proofread

model:
    name: gpt-5
    temperature: 0.7
    max_tokens: 1024
```

🤖🤖🤖 **Multi-tasker Example** [(config file ↗)](config/multi.yaml)
```yaml
model:
    translate:
        name: gpt-4.1
        temperature: 0.7
        max_tokens: 1024
    postedit:
        name: gpt-4o
        temperature: 0.7
        max_tokens: 1024
    name: gpt-5
        temperature: 0.7
        max_tokens: 1024
```

### ➡ Prepare your data
Input data must be provided as a CSV file. The required columns for all modes are:
- src_lang
- tgt_lang
- src_text

Additional notes:
- `target` is optional for Translation Agent, but is obligatory to Post-edit & Proofread Agents to use it as the initial hypothesis
- During multi-task execution, agents iteratively upate the `target` field.
- **If you already have a translation, you can skip the Translate Agent** by setting `skip_translate_if_provided: true` in your configuration. ✅
  - In **multi-task mode**: skips the translate step and directly proceeds to postedit → proofread
  - In **single-task mode** (postedit/proofread): returns the existing translation without processing

**Example: Skip Translate Agent**
```yaml
# Enable skipping translate when translation is already provided
skip_translate_if_provided: true

model:
    translate:
        name: gpt-4.1
        temperature: 0.7
        max_tokens: 1024
    # ... other model configs
```

**Example CSV format**
|||||||
|-|-|-|-|-|-|
|src_lang|tgt_lang|src_text|**target**|ref_text|domain|
|...|...|...|...|...|...|

# ✺ Input & Output
🧑‍🏫 **Source**: 你永远主动联系不上这个专员，也不知道她的工号，也没有直线联系电话，就是你联系不上她，只有她联系你。

🧑‍🏫 **Reference**: Since you don't know the commissioner's job number and there isn't a direct phone number to call, you'll never make the effort to get in touch with her, She is the only one who can reach you, You can't.

🤖 **Translation**: You never actively contact the commissioner, you never know her job number, you never have a direct telephone line, you never contact her, she only contacts you.

🤖 **Postedit**: You can never proactively reach this specialist. You don't know her employee ID, nor do you have a direct phone number. It's always that you cannot contact her; only she can contact you.

🤖 **Proofread**: You can never proactively contact the commissioner, you never know her employee ID, you never have a direct telephone line, you cannot reach her, she only contacts you.

🤖🤖🤖 **Multi-agent Translation**: You can never proactively reach this commissioner, as you don’t know her employee ID or have a direct phone number; only she contacts you, and you cannot get in touch with her.

# ✺ Project Structure
```
Multi-AgentMT/
├─ agents/
│  ├─ run.py                 # CLI entry point
│  ├─ core/
│  │  ├─ engine.py           # Async batch execution engine
│  │  └─ call_api.py         # Async OpenAI API wrapper
│  ├─ modules/
│  │  ├─ singletasker.py     # Single-task execution
│  │  └─ multitasker.py      # Multi-task pipeline
│  │  └─ dispatcher/         # Prompt & parameter dispatch
│  ├─ parser/                # Output parsing
│  └─ prompt/                # Prompt templates
│
├─ rubric_mqm/               # (submodule) MQM evaluation toolkit
│  └─ metric/
│
├─ data/
│  └─ sample.csv
│
└─ agents/config/
   ├─ single.yaml
   └─ multi.yaml
```

# ✺ Citation
If you use this framework in your research or projects, please cite it as follows:

```
@inproceedings{kim-2025-multi,
    title = "Multi-agent{MT}: Deploying {AI} Agent in the {WMT}25 Shared Task",
    author = "Kim, Ahrii",
    editor = "Haddow, Barry  and
      Kocmi, Tom  and
      Koehn, Philipp  and
      Monz, Christof",
    booktitle = "Proceedings of the Tenth Conference on Machine Translation",
    month = nov,
    year = "2025",
    address = "Suzhou, China",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2025.wmt-1.53/",
    doi = "10.18653/v1/2025.wmt-1.53",
    pages = "769--777",
    ISBN = "979-8-89176-341-8",
    abstract = "We present Multi-agentMT, our system for the WMT25 General Shared Task. The model adopts Prompt Chaining, a multi-agent workflow combined with Rubric-MQM, an automatic MQM-based error annotation metric. Our primary submission follows a Translate{--}Postedit{--}Proofread pipeline, in which error positions are explicitly marked and iteratively refined. Results suggest that a semi-autonomous agent scheme for machine translation is feasible with a smaller, earlier-generation model in low-resource settings, achieving comparable quality at roughly half the cost of larger systems."
}

@inproceedings{kim-2025-preliminary,
    title = "A Preliminary Study of {AI} Agent Model in Machine Translation",
    author = "Kim, Ahrii",
    editor = "Haddow, Barry  and
      Kocmi, Tom  and
      Koehn, Philipp  and
      Monz, Christof",
    booktitle = "Proceedings of the Tenth Conference on Machine Translation",
    month = nov,
    year = "2025",
    address = "Suzhou, China",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2025.wmt-1.32/",
    doi = "10.18653/v1/2025.wmt-1.32",
    pages = "583--586",
    ISBN = "979-8-89176-341-8",
    abstract = "We present IR{\_}Multi-agentMT, our submission to the WMT25 General Shared Task. The system adopts an AI-agent paradigm implemented through a multi-agent workflow, Prompt Chaining, in combination with RUBRIC-MQM, an automatic MQM-based error annotation metric. Our primary configuration follows the Translate{--}Postedit{--}Proofread paradigm, where each stage progressively enhances translation quality. We conduct a preliminary study to investigate (i) the impact of initial translation quality and (ii) the effect of enforcing explicit responses from the Postedit Agent. Our findings highlight the importance of both factors in shaping the overall performance of multi-agent translation systems."
}
```

# ✺ [License](LICENSE)