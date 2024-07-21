from PyInstaller.utils.hooks import collect_submodules

hidden_imports = collect_submodules('parser')