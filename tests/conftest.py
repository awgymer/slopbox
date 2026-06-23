from pathlib import Path

import copier
import pytest

TEMPLATE_ROOT = Path(__file__).parent.parent


@pytest.fixture
def render(tmp_path):
    """Render the template into tmp_path with the given answers."""

    def _render(**answers):
        copier.run_copy(
            src_path=str(TEMPLATE_ROOT),
            dst_path=str(tmp_path),
            data=answers,
            defaults=True,
            overwrite=True,
            unsafe=True,
            quiet=True,
            # Render the current working tree (HEAD + uncommitted changes)
            # rather than copier's default of the latest git tag, so tests
            # validate in-development template changes.
            vcs_ref="HEAD",
        )
        return tmp_path

    return _render
