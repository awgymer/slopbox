import json

import yaml

NEXTFLOW_ATOMS = ["java", "nextflow", "nf-test", "uv", "nf-core"]
AWS_ATOMS = ["node", "aws-cdk", "awscli"]


def _answers(dst):
    return yaml.safe_load((dst / ".copier-answers.yml").read_text())


def _install_root(dst):
    return (dst / ".devcontainer/claude/installers/install-root.sh").read_text()


def _install_user(dst):
    return (dst / ".devcontainer/claude/installers/install-user.sh").read_text()


def _firewall(dst):
    return (dst / "extra-allowed-domains").read_text()


def _extensions(dst):
    spec = json.loads((dst / ".devcontainer/claude/devcontainer.json").read_text())
    return spec["customizations"]["vscode"]["extensions"]


def test_empty_selection(render):
    dst = render(extra_tools=[])
    assert _answers(dst)["installed_tools"] == []
    assert "astral.sh/uv" not in _install_user(dst)
    assert "temurin" not in _install_root(dst)
    assert _extensions(dst) == [
        "anthropic.claude-code",
        "esbenp.prettier-vscode",
        "eamodio.gitlens",
    ]


def test_uv_alone(render):
    dst = render(extra_tools=[["uv"]])
    assert _answers(dst)["installed_tools"] == ["uv"]
    assert "https://astral.sh/uv/install.sh" in _install_user(dst)
    fw = _firewall(dst)
    assert "pypi.org" in fw
    assert "files.pythonhosted.org" in fw
    exts = _extensions(dst)
    assert "ms-python.python" in exts
    assert "charliermarsh.ruff" in exts


def test_java_alone(render):
    dst = render(extra_tools=[["java"]])
    assert _answers(dst)["installed_tools"] == ["java"]
    assert "temurin-21-jdk" in _install_root(dst)
    assert "vscjava.vscode-java-pack" in _extensions(dst)


def test_rust_alone(render):
    dst = render(extra_tools=[["rust"]])
    assert _answers(dst)["installed_tools"] == ["rust"]
    assert "https://sh.rustup.rs" in _install_user(dst)
    fw = _firewall(dst)
    assert "crates.io" in fw
    assert "static.rust-lang.org" in fw
    assert "rust-lang.rust-analyzer" in _extensions(dst)


def test_nextflow_bundle(render):
    dst = render(extra_tools=[NEXTFLOW_ATOMS])
    assert set(_answers(dst)["installed_tools"]) == set(NEXTFLOW_ATOMS)

    root = _install_root(dst)
    assert "temurin-21-jdk" in root
    assert "/usr/local/bin/nextflow" in root

    user = _install_user(dst)
    assert "https://astral.sh/uv/install.sh" in user
    assert "uv tool install" in user
    assert "get.nf-test.com" in user
    assert "nextflow info" in user

    fw = _firewall(dst)
    assert "nf-co.re" in fw
    assert "docs.seqera.io" in fw

    exts = _extensions(dst)
    for expected in [
        "nextflow.nextflow",
        "editorconfig.editorconfig",
        "gruntfuggly.todo-tree",
        "redhat.vscode-yaml",
        "mechatroner.rainbow-csv",
        "oderwat.indent-rainbow",
    ]:
        assert expected in exts


def test_aws_bundle(render):
    dst = render(extra_tools=[AWS_ATOMS])
    assert set(_answers(dst)["installed_tools"]) == set(AWS_ATOMS)

    root = _install_root(dst)
    assert "awscli-exe-linux" in root

    user = _install_user(dst)
    assert "nvm-sh/nvm" in user
    assert "npm install -g aws-cdk" in user

    fw = _firewall(dst)
    assert "sts.amazonaws.com" in fw
    assert "docs.aws.amazon.com" in fw
    assert "nodejs.org" in fw

    assert "amazonwebservices.aws-toolkit-vscode" in _extensions(dst)


def test_uv_plus_nextflow_bundle_dedupes(render):
    dst = render(extra_tools=[["uv"], NEXTFLOW_ATOMS])
    atoms = _answers(dst)["installed_tools"]
    assert atoms.count("uv") == 1
    assert set(atoms) == set(NEXTFLOW_ATOMS)


def test_both_bundles(render):
    dst = render(extra_tools=[NEXTFLOW_ATOMS, AWS_ATOMS])
    assert set(_answers(dst)["installed_tools"]) == set(NEXTFLOW_ATOMS) | set(AWS_ATOMS)
