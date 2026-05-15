# Claude Code Devcontainer Sandbox

A template for running Claude Code inside a sandboxed devcontainer, intended for use with `--dangerously-skip-permissions`. The container runs as an unprivileged user with an egress firewall that restricts outbound traffic to a known allowlist.

Based on the [official Anthropic devcontainer example](https://github.com/anthropics/claude-code/tree/main/.devcontainer).

## Requirements

- VS Code with the [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)
- Docker
- [Copier](https://copier.readthedocs.io/) (`pipx install copier`)
- A GitHub personal access token with repo access

## Setup

From your project directory, run:

```bash
copier copy gh:awgymer/slopbox .
```

Copier will ask for a parent directory (default: `.devcontainer`) and a container name (default: `claude`), then install the files into `<devcontainer_root>/<name>/`.

Add `devcontainer.env` to your `.gitignore`, then open it at your project root and fill in your values:

```
GH_TOKEN=           # GitHub personal access token
GIT_AUTHOR_NAME=    # Your name for git commits
GIT_AUTHOR_EMAIL=   # Your email for git commits
GIT_COMMITTER_NAME=
GIT_COMMITTER_EMAIL=
```

Open the project in VS Code and select **Reopen in Container**.

## Updating

To pull in template changes while keeping your local modifications:

```bash
copier update
```

Copier performs a 3-way merge, so changes to files like the `Dockerfile` are reconciled with your own additions. `devcontainer.env` is never overwritten.

Commit `.copier-answers.yml` to your repo so teammates can also run `copier update`.

## Firewall

The container restricts outbound traffic to a fixed allowlist on startup. To permit additional domains, add them space-separated to `devcontainer.env`:

```
EXTRA_ALLOWED_DOMAINS="pypi.org api.mycompany.com"
```

## Customisation

- **Add tools**: install them in the `Dockerfile` after the marked section
- **Shell config**: edit `zshrc` in your chosen install directory before starting the container
- **Prompt**: replace `p10k.zsh` with your own Powerlevel10k config
