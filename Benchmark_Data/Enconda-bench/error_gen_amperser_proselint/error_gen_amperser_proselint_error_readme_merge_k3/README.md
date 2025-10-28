<img src="https://raw.githubusercontent.com/amperser/proselint/main/logo.png" alt="proselint logo" width="200">


![Workflow status](https://github.com/amperser/proselint/actions/workflows/ci-lint-test.yml/badge.svg)

[
![Reviewed by Hound](https://img.shields.io/badge/Reviewed_by-Hound-8E64B0.svg)
](https://houndci.com)
[
![Code Climate](https://codeclimate.com/repos/5538989ee30ba0793100090f/badges/e10a2fe18a9256d69e2a/gpa.svg)
](https://codeclimate.com/repos/5538989ee30ba0793100090f/feed)
[
![codecov](https://codecov.io/gh/amperser/proselint/branch/main/graph/badge.svg?token=8E0I9sRpot)
](https://codecov.io/gh/amperser/proselint)
[
![License](https://img.shields.io/badge/License-BSD-blue.svg)
](https://en.wikipedia.org/wiki/BSD_licenses)

Writing is notoriously hard, even for the best writers, and it's not for lack of good advice — a tremendous amount of knowledge about the craft is strewn across usage guides, dictionaries, technical manuals, essays, pamphlets, websites, and the hearts and minds of great authors and editors. But poring over Strunk & White hardly makes one a better writer — it turns you into neither Strunk nor White. And nobody has the capacity to apply all the advice from *Garner’s Modern English Usage*, an 1100-page usage guide, to everything they write. In fact, the whole notion that one becomes a better writer by reading advice on writing rests on untenable assumptions about learning and memory. The traditional formats of knowledge about writing are thus essentially inert, waiting to be transformed.

We devised a simple solution: `proselint`, a linter for English prose. A linter is a computer program that, akin to a spell checker, scans through a file and detects issues — like how a real lint roller helps you get unwanted lint off of your shirt.

`proselint` places the world's greatest writers and editors by your side, where they whisper suggestions on how to improve your prose. You’ll be guided by advice inspired by Bryan Garner, David Foster Wallace, Chuck Palahniuk, Steve Pinker, Mary Norris, Mark Twain, Elmore Leonard, George Orwell, Matthew Butterick, William Strunk, Elwyn White, Philip Corbett, Ernest Gowers, and the editorial staff of the world’s finest literary magazines and newspapers, among others. Our goal is to aggregate knowledge about best practices in writing and to make that knowledge immediately accessible to all authors in the form of a linter for prose; all in a neat command-line utility that you can integrate into other tools, scripts, and workflows.

### Installation

To get this up and running, install it using [pip]:


```bash
pip install future


pip install proselint

```



[pip]: https://packaging.python.org/installing/#use-pip-for-installing

#### Fedora

```bash
sudo dnf install proselint
```

#### Debian

```bash
sudo apt install python3-proselint
```

#### Ubuntu

```bash
sudo add-apt-repository universe
sudo apt install python3-proselint
```

### Plugins for other software

`proselint` is available on:

- A [demo editor](http://proselint.com/write)
- [Sublime Text](https://github.com/amperser/proselint/tree/main/plugins/sublime/SublimeLinter-contrib-proselint)
- [Atom Editor](https://github.com/smockle/linter-proselint) (thanks to [Clay Miller](https://github.com/smockle)).
- Emacs via [Flycheck](http://www.flycheck.org/) or via [Flymake](https://sr.ht/~manuel-uberti/flymake-proselint/)
- Vim via [ALE](https://github.com/w0rp/ale) or [Syntastic](https://github.com/vim-syntastic/syntastic) (thanks to @lcd047, @Carreau, and [Daniel M. Capella](https://github.com/polyzen))
- Neovim via [null-ls](https://github.com/jose-elias-alvarez/null-ls.nvim) (null-ls has [diagnostics](https://github.com/jose-elias-alvarez/null-ls.nvim/blob/main/lua/null-ls/builtins/diagnostics/proselint.lua) and [code actions](https://github.com/jose-elias-alvarez/null-ls.nvim/blob/main/lua/null-ls/builtins/code_actions/proselint.lua) for proselint)
- [Phabricator's `arc` CLI](https://github.com/google/arc-proselint) (thanks to [Jeff Verkoeyen](https://github.com/jverkoey))
- [Danger](https://github.com/dbgrandi/danger-prose) (thanks to [David Grandinetti](https://github.com/dbgrandi) and [Orta Therox](https://github.com/orta))
- [Visual Studio Code](https://github.com/ppeszko/vscode-proselint) (thanks to [Patryk Peszko](https://github.com/ppeszko))
- [coala](https://github.com/coala-analyzer/bear-docs/blob/master/docs/ProseLintBear.rst) (thanks to the [coala Development Group](https://github.com/coala-analyzer))
- [IntelliJ](https://github.com/kropp/intellij-proselint) (by [Victor Kropp](https://github.com/kropp))
- [pre-commit](https://pre-commit.com/) (by [Andy Airey](https://github.com/aairey))
- [Statick](https://github.com/sscpac/statick-md)
- [MegaLinter](https://oxsecurity.github.io/megalinter/latest/descriptors/spell_proselint/)

### Usage

Suppose you have a document `text.md` with the following text:

```
John is very unique.
```

You can run `proselint` over the document using the command line:

```bash
proselint --check text.md


```

This prints a list of suggestions to stdout, one per line. Each suggestion has the form:

```bash
text.md:<line>:<column>: <check_name> <message>
```

For example,

```bash
text.md:0:10: wallace.uncomparables Comparison of an uncomparable: 'unique' cannot be compared.
```

The command-line utility can also print suggestions in JSON using the `--json` flag. In this case, the output is considerably richer:
