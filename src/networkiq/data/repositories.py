from pathlib import Path

import pandas as pd


class NetworkRepository:
    """Repository for accessing telecom network data."""

    def __init__(self, data_dir: Path):
        self.data_dir = data_dir

        self.kpis_path = data_dir / "network_kpis.csv"
        self.cells_path = data_dir / "cells.csv"
        self.incidents_path = data_dir / "incidents.csv"

        self._kpis = pd.read_csv(self.kpis_path)
        self._cells = pd.read_csv(self.cells_path)
        self._incidents = pd.read_csv(self.incidents_path)

    def get_kpis(
        self,
        cell_id: str | None = None,
        region: str | None = None,
    ) -> pd.DataFrame:
        """Return KPI records filtered by cell and/or region."""

        df = self._kpis.copy()

        if cell_id:
            df = df[df["cell_id"] == cell_id]

        if region:
            df = df[df["region"] == region]

        return df

    def get_cell(self, cell_id: str) -> pd.DataFrame:
        """Return metadata for a specific cell."""

        return self._cells[
            self._cells["cell_id"] == cell_id
        ].copy()

    def get_incidents(
        self,
        cell_id: str | None = None,
    ) -> pd.DataFrame:
        """Return historical incidents."""

        df = self._incidents.copy()

        if cell_id:
            df = df[df["cell_id"] == cell_id]

        return df