# Contributor guidelines

You can contribute to this project by creating 
[issues](https://github.com/mever-team/transparency-service/issues) 
that include both bugs and enhancements, or submitting new code 
in the form of a pull request. These guidelines cover:

[How to create an issue](#how-to-create-an-issue)<br>
[How to submit a pull request (PR)](#how-to-submit-a-pull-request-pr)<br>
[LLM coding policy](#llm-coding-policy)<br>
[Code of conduct](#code-of-conduct)

## How to create an issue

- Make sure that the issue title properly summarizes what is requested from this project.
- Make a complete point, for example by uploading screen snippets or instructions of how to induce some behavior.
- Contrast current vs expected behavior.

You can use a free text format similar to #27 , 
or make it more concrete using this template:

```text
**Title:**
your issue title

**About:**
Summarize what you are proposing in one or two sentences. 
This is a good point to mention -if you want- why you think this issue is important.

**Replicate:**
Describe how to reach a specific state for which you want to talk.

**Current:**
Perceived existing behavior.

**Proposal:** 
You can state that the result is a bug, that it could be or look different/have more options (describe them), or that related functionality is missing.
```

## How to submit a pull request (PR)

Fork this repository's `dev` branch, create a branch for your changes and, 
once you have pushed new code, create a PR towards this repository's 
`dev` branch again. 

Instructions to bootstrap development should look something like this:

```commandline
cd transparency-service
git checkout -b MYFEATURE
python -m venv .venv
source .venv/bin/activate
pip install -e package
python -m examples.demo
```

Make sure that the PR's description explains new or changed
functionality to the degree that a code reviewer can understand
them. It is preferred to have 
created an issue beforehand (see above) that clearly 
indicates your intent to provide a contribution. Then,
preliminary and code design can be aligned via discussion
in that issue.

## LLM coding policy

LLM-generated code is easy to spot, especially if it has not
been touched up. It is also bound to create unforeseen effects if
not properly controlled. We ask contributors to methodically go 
through such outputs and properly review them. Even useful PRs may 
be rejected outright if they create code significantly misaligned
with this repository, indicating that there has been little user 
oversight.

Problematic patterns include but are not limited to: 
too many changes without justifiable need, 
perfunctory changes/refactors (the maintainers
are responsible for such activities), lack of early returns or of asserts
in case of failed preconditions, excessive nesting, useless comments
describing the "what" but not "why", excessive helper functions,
excessively verbose variable and function names, and broader security 
concerns. For Python code, in particular, docstrings for trivially 
obvious functions are forbidden.

Of course, nobody is perfect, and this is taken into account. The
above list is just so that we can have a frame of discussion.

That said, autonomous bot contributors will be outright banned, 
unless their usage has been agreed to beforehand.

## Code of conduct

We adhere to the [contributor covenant](https://www.contributor-covenant.org/).
If you encounter restricted behaviors like harassment or character attacks,
you may reach out via email to the maintainers whose contact information is 
listed in this repository's [README](README.md) 
(add all maintainers as email recepients). You will remain anonymous,
regardless of the action taken.