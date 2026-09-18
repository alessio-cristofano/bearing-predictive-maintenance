"""Schemas definition for dataset specs."""

from dataclasses import dataclass
from typing import ClassVar


@dataclass(frozen=True)
class DatasetSpec:
    """Immutable specification contract for an individual test run.

    Attributes:
        dataset_id: Numerical identifier of the dataset (1, 2, or 3).
        column_names: Ordered channel names representing physical sensor
            placements across the bearing test rig.
        expected_rows: Total sample points captured per 1-second snapshot
            sampled at 20 kHz.
    """

    dataset_id: int
    column_names: list[str]
    expected_rows: ClassVar[int] = 20480

    @classmethod
    def get_rows(cls) -> int:
        """Return the expected row count per snapshot file.

        Returns:
            int: The constant snapshot sample height (20,480 points).
        """
        return cls.expected_rows


SPECS: dict[int, DatasetSpec] = {
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
