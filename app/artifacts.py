"""Versioned model-artifact storage boundary.

The local filesystem backend is the only enabled implementation in this
educational build. Cloud object-storage adapters must preserve the same
version/checksum contract and require a separate deployment approval.
"""
from pathlib import Path

import joblib


class ArtifactStore:
    backend = "local-filesystem"

    def __init__(self, root):
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)

    def path(self, version):
        return self.root / f"model_v{version}.joblib"

    def save(self, model, version):
        joblib.dump(model, self.path(version))
        return self.path(version)

    def exists(self, version):
        return self.path(version).exists()

    def load(self, version):
        return joblib.load(self.path(version))
