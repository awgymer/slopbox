# Claude Code Devcontainer Sandbox

A template for running Claude Code inside a sandboxed devcontainer, intended for use with `--dangerously-skip-permissions`. The container runs as an unprivileged user with an egress firewall that restricts outbound traffic to a known allowlist.

Based on the [official Anthropic devcontainer example](https://github.com/anthropics/claude-code/tree/main/.devcontainer).

## Requirements

- VS Code with the [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)
- Docker
- [Copier](https://copier.readthedocs.io/) (e.g. `uv tool install copier`)
- A GitHub personal access token with repo access

## Setup

From your project directory, run:

```bash
copier copy gh:awgymer/slopbox .
```

Copier will ask for:
- a parent directory (default: `.devcontainer`),
- a container name (default: `claude`),
- an optional set of extra tools to install (see [Optional tools](#optional-tools)).

The files are installed into `<devcontainer_root>/<name>/`.

Add `devcontainer.env` to your `.gitignore`, then open it at your project root and fill in your values:

```
GH_TOKEN=           # GitHub personal access token
GIT_AUTHOR_NAME=    # Your name for git commits
GIT_AUTHOR_EMAIL=   # Your email for git commits
GIT_COMMITTER_NAME=
GIT_COMMITTER_EMAIL=
```

Open the project in VS Code and select **Reopen in Container**.

## Optional tools

During `copier copy` you can multi-select extra tools to install in the container:

- **uv** — Python package manager (Astral)
- **Java (Temurin 21)** — JDK from Adoptium
- **Rust (rustup)** — Rust toolchain (`rustc`, `cargo`) via rustup
- **nextflow-bundle** — `java`, `nextflow`, `nf-test`, `uv`, `nf-core` (with `prek` and `pre-commit`)
- **aws-bundle** — `node` (via nvm), `aws-cdk`, `awscli`

Bundles install dependencies automatically; selecting multiple choices dedupes. The resolved atomic tool list is stored as `installed_tools` in `.copier-answers.yml`.

### Version overrides

Defaults are pinned in the installer scripts. To override at build time, pass build args to Docker or edit `build.args` in `devcontainer.json`:

| Tool      | ARG                | Default   |
|-----------|--------------------|-----------|
| Nextflow  | `NEXTFLOW_VERSION` | `25.10.4` |
| nf-test   | `NFT_VERSION`      | `0.9.5`   |
| nf-core   | `NFCORE_VERSION`   | `3.5.1`   |
| node      | `NODE_VERSION`     | `22`      |

### Firewall additions

Selecting a tool that needs runtime network access auto-adds the relevant domains to `extra-allowed-domains`:

- `uv` → `pypi.python.org`, `pypi.org`, `pythonhosted.org`, `files.pythonhosted.org`
- `node` → `nodejs.org`
- `rust` → `static.rust-lang.org`, `crates.io`, `index.crates.io`, `static.crates.io`
- `nextflow` → `nf-co.re`, `docs.seqera.io`
- `awscli` → `sts.amazonaws.com` (add service-specific endpoints as needed)

## Updating

To pull in template changes while keeping your local modifications:

```bash
copier update
```

Copier performs a 3-way merge, so changes to files like the `Dockerfile` are reconciled with your own additions. `devcontainer.env` is never overwritten.

Commit `.copier-answers.yml` to your repo so teammates can also run `copier update`.

## Firewall

The container restricts outbound traffic to a fixed allowlist on startup. To permit additional domains, add them to `extra-allowed-domains` at your project root, one per line:

```
# extra-allowed-domains
pypi.org
api.mycompany.com
```

Lines starting with `#` and blank lines are ignored.

## Customisation

- **Add tools**: pick from the prebuilt set via the `extra_tools` copier question (see [Optional tools](#optional-tools)), or add custom installs in `Dockerfile`
- **Shell config**: edit `zshrc` in your chosen install directory before starting the container
- **Prompt**: replace `p10k.zsh` with your own Powerlevel10k config
