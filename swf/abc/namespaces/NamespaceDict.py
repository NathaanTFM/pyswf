from __future__ import annotations
from .BaseNamespace import BaseNamespace
from .Namespace import Namespace
from .PackageNamespace import PackageNamespace
from .PackageInternalNs import PackageInternalNs
from .ProtectedNamespace import ProtectedNamespace
from .ExplicitNamespace import ExplicitNamespace
from .StaticProtectedNs import StaticProtectedNs
from .PrivateNs import PrivateNs

NamespaceDict: dict[int, type[BaseNamespace]] = {
    Namespace.kind: Namespace,
    PackageNamespace.kind: PackageNamespace,
    PackageInternalNs.kind: PackageInternalNs,
    ProtectedNamespace.kind: ProtectedNamespace,
    ExplicitNamespace.kind: ExplicitNamespace,
    StaticProtectedNs.kind: StaticProtectedNs,
    PrivateNs.kind: PrivateNs
}

__all__ = [
    'BaseNamespace',
    'Namespace',
    'PackageNamespace',
    'PackageInternalNs',
    'ProtectedNamespace',
    'ExplicitNamespace',
    'StaticProtectedNs',
    'PrivateNs',
    'NamespaceDict'
]