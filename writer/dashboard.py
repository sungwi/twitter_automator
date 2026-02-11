from pathlib import Path

from .templates import DASHBOARD_TEMPLATE


class DashboardWriter:
    def __init__(self, vault_path: str):
        self.base_path = Path(vault_path) / "TwitterLikes"

    def write_dashboard(self) -> Path:
        self.base_path.mkdir(parents=True, exist_ok=True)
        dashboard_path = self.base_path / "Dashboard.md"
        dashboard_path.write_text(DASHBOARD_TEMPLATE)
        return dashboard_path
