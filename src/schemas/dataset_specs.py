from dataclasses import dataclass
from typing import ClassVar


@dataclass(frozen=True)
class DatasetSpec:
    dataset_id: int
    column_names: list[str]
    expected_rows: ClassVar[int] = 20480

    @classmethod
    def get_rows(cls) -> int:
        """Returns the expected number of rows for any dataset snapshot"""
        return cls.expected_rows


SPECS = {
    1: DatasetSpec(
        dataset_id=1,
        column_names=["b1_x", "b1_y", "b2_x", "b2_y", "b3_x", "b3_y", "b4_x", "b4_y"],
    ),
    2: DatasetSpec(
        dataset_id=2,
        column_names=["b1", "b2", "b3", "b4"],
    ),
    3: DatasetSpec(
        dataset_id=3,
        column_names=["b1", "b2", "b3", "b4"],
    ),
}
