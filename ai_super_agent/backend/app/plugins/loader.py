from __future__ import annotations

import importlib.util
import os
from pathlib import Path
from typing import Iterable, Optional

from fastapi import FastAPI

from backend.app.config import Settings
from backend.app.plugins.plugin_base import BasePlugin, PluginMeta


def iter_plugin_paths(plugin_dirs: Iterable[str]) -> Iterable[Path]:
	for directory in plugin_dirs:
		path = Path(directory)
		if not path.exists() or not path.is_dir():
			continue
		for child in path.iterdir():
			if child.is_dir():
				plugin_file = child / "plugin.py"
				if plugin_file.exists():
					yield plugin_file


def load_module_from_path(name: str, path: Path):
	spec = importlib.util.spec_from_file_location(name, str(path))
	if spec is None or spec.loader is None:
		raise ImportError(f"Cannot load spec for {path}")
	module = importlib.util.module_from_spec(spec)
	spec.loader.exec_module(module)  # type: ignore
	return module


def build_default_mount_path(meta: PluginMeta) -> str:
	return meta.mount_path or f"/plugins/{meta.name}"


def load_plugins(app: FastAPI, settings: Settings) -> None:
	for plugin_path in iter_plugin_paths(settings.plugin_dirs):
		module_name = f"plugin_{plugin_path.parent.name}"
		try:
			module = load_module_from_path(module_name, plugin_path)
			if not hasattr(module, "get_plugin"):
				print(f"[plugins] Skipping {plugin_path}, missing get_plugin()")
				continue
			plugin: BasePlugin = module.get_plugin(app=app, settings=settings)  # type: ignore
			mount_path = build_default_mount_path(plugin.meta)
			app.include_router(plugin.get_router(), prefix=mount_path, tags=[f"plugin:{plugin.meta.name}"])
			print(f"[plugins] Loaded {plugin.meta.name} v{plugin.meta.version} at {mount_path}")
		except Exception as exc:
			print(f"[plugins] Failed loading {plugin_path}: {exc}")