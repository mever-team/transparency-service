[![Build](https://github.com/mever-team/transparency-service/actions/workflows/build.yml/badge.svg?branch=dev)](https://github.com/mever-team/transparency-service/actions/workflows/build.yml) 
![License](https://img.shields.io/badge/license-Apache--2.0-blue)
# AI Card

*A model card catalogue. Host it yourself, or browse the public database. Create and access cards from the browser or your experiment tracking code.*

![screenshot](ui/transparency/img/handbook/readers2.webp)

1. Select a model card catalogue. Temporarily host one 
locally as a service with minimal setup that you can access
from a browser-based UI, or use our public service at
[trai.mever.gr](https://trai.mever.gr/).

2. Install *aicard* in a Python environment 
and then link to the catalogue for creating a new model card
storing your model's properties:

```python
import aicard as aic

conn = aic.connect("https://trai.mever.gr/", username="myname", password="mypassword", silent=True)
with conn.create() as card:
    card.title = "my new card"
```

## 🔥 Features

- Browse model cards.
- See missing information that would help non-experts.
- Lightweight deterministic question-answering. Example: "Is this model safe for usage by minors?"
- Ollama integration to let help from LLMs in refining the cards.
- Automate card upload from your existing model testing pipeline.

## 🔗 Material

- [Create and upload cards programmatically](docs/create.md)
- [Host a local server](docs/host.md)
- [UI guide](https://trai.mever.gr/transparency/handbook.html)
- [Contributor guidelines](CONTRIBUTING.md)

## 📜 About

**Maintainers**<br>
Emmanouil Krasanakis - maniospas@iti.gr<br>
Giorgos Nikoulis - gnikoul@iti.gr<br>
Lazaros Apostolidis - laaposto@iti.gr


**License**<br>
Apache 2.0

```
Copyright 2025-2026 mever.gr

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied. See the License for the specific language governing
permissions and limitations under the License.
```
