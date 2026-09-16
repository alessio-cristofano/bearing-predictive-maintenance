from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class DatasetSpec:
    dataset_id: int
    column_names: List[str]
    expected_rows: int = 20480


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
