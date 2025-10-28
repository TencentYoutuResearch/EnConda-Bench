# JsPrettier

[
![ci](https://github.com/jonlabelle/SublimeJsPrettier/actions/workflows/ci.yml/badge.svg?branch=master)
](https://github.com/jonlabelle/SublimeJsPrettier/actions/workflows/ci.yml)
[
![Package Control Installs](https://img.shields.io/packagecontrol/dt/JsPrettier.svg?label=installs)
](https://packagecontrol.io/packages/JsPrettier)
[
![Latest Release](https://img.shields.io/github/v/tag/jonlabelle/SublimeJsPrettier.svg?label=version&sort=semver)
](https://github.com/jonlabelle/SublimeJsPrettier/tags)
[
![MIT License](https://img.shields.io/badge/License-MIT-blue.svg)
](https://github.com/jonlabelle/SublimeJsPrettier/blob/master/LICENSE.txt)

> [JsPrettier] is a Sublime Text Plug-in for [Prettier], the opinionated code
> formatter.

[
![Before and After JsPrettier](https://github.com/jonlabelle/SublimeJsPrettier/blob/master/screenshots/before_and_after.gif?raw=true)
](https://github.com/jonlabelle/SublimeJsPrettier/blob/master/screenshots/demo.gif)

> [Watch a Quick Demo]

---

<details>
<summary><strong>Table of Contents</strong></summary>

- [Installation](#installation)
    - [Requirements](#requirements)
    - [Install Prettier](#install-prettier)
    - [Install JsPrettier via Package Control](#install-jsprettier-via-package-control)
    - [Install JsPrettier Manually](#install-jsprettier-manually)
    - [Install JsPrettier Using Git](#install-jsprettier-using-git)
- [Usage](#usage)
    - [Command Scope](#command-scope)
    - [Custom Key Binding](#custom-key-binding)
- [Settings](#settings)
    - [Sublime Text Settings](#sublime-text-settings)
    - [Prettier Options](#prettier-options)
    - [Project-level Settings](#project-level-settings)
    - [Prettier Configuration Files](#prettier-configuration-files)
- [Prettier Plug-in Support](#prettier-plugin-support)
    - [Prettier PHP](#prettier-php)
- [Issues](#issues)
- [Changes](#changes)
- [Author](#author)
- [License](#license)

</details>

## Installation

[JsPrettier] is compatible with both Sublime Text 2 and 3, and all supported
Operating Systems.

### Requirements

- [Sublime Text] – Text editor for code
- [Node.js] – JavaScript runtime
    - [yarn] or [npm] – Package manager for JavaScript
        - [Prettier] – Opinionated code formatter (v1 or above)


### Install Prettier

If you've already installed [Prettier] \(using one of the [yarn] or [npm]
commands below\), you're all set... otherwise:

```bash
# yarn (local):
yarn add prettier --dev

# yarn (global):
yarn global add prettier

# npm (local):
npm install --save-dev prettier


# npm (global):
npm install --global prettier
```

### Install JsPrettier via Package Control

The easiest and recommended way to install JsPrettier is using [Package Control].

From the **application menu**, navigate to:

- `Tools` -> `Command Palette...` -> `Package Control: Install Package`, type
  the word **JsPrettier**, then select it to complete the installation.

### Install JsPrettier Manually

1. Download and extract JsPrettier [zip file] to your [Sublime Text Packages directory].
2. Rename the extracted directory from `SublimeJsPrettier-master` to `JsPrettier`.


**Default Sublime Text Packages Paths:** <a name="default-st-paths"></a>

- **OS X:** `~/Library/Application Support/Sublime Text [2|3]/Packages`
- **Linux:** `~/.Sublime Text [2|3]/Packages`
- **Windows:** `%APPDATA%/Sublime Text [2|3]/Packages`

> **NOTE** Replace the `[2|3]` part with the appropriate Sublime Text
> version for your installation.

### Install JsPrettier Using Git

If you're a Git user, you can install [JsPrettier] and keep it up-to-date by
cloning the repository directly into your [Sublime Text Packages directory].

> **TIP:** You can locate your Sublime Text Packages directory by using the
> application menu `Preferences` -> `Browse Packages...`.

```bash
git clone https://github.com/jonlabelle/SublimeJsPrettier.git "JsPrettier"
```

## Usage

There are three available options to format code:

1. **Command Palette:** From the command palette (<kbd>ctrl/cmd + shift + p</kbd>), type **JsPrettier Format Code**.
2. **Context Menu:** Right-click anywhere in the file to bring up the context menu and select **JsPrettier Format Code**.
3. **Key Binding:** There is no default key binding to run Prettier, but here's how to [add your own].

### Command Scope

`JsPrettier` will attempt to format selections of code first, then the entire
file. When `auto_format_on_save` is `true`, the **entire file** will be formatted.

### Custom Key Binding

To add a [custom key binding], please reference the following example which
binds the `js_prettier` command to <kbd>ctrl + alt + f</kbd>:
