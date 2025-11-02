```mermaid
classDiagram
    direction LR

    class Benchmark {
        -results : list
        +Run(sort_function, data, name, condition) void
        +CheckSorted(arr) bool
        +DisplayResults() list~string~
    }

    class DataGenerator {
        -seed : int
        -max_duration : int
        +GenerateRecords(size) list~TreatmentRecord~
        +GetRandom(size) list~TreatmentRecord~
        +GetSorted(size) list~TreatmentRecord~
        +GetReversed(size) list~TreatmentRecord~
        +GetNearlySorted(size) list~TreatmentRecord~
    }

    class TreatmentRecord {
        +patient_id : int
        +duration : int
        +__repr__() string
    }

    class SortStats {
        +comparisons : int
        +swaps : int
        +__repr__() string
    }

    class SortUtils ["Sort Utilities (Component)"] {
        +mergeSort(arr, stats) void
        +quickSortMedian3(arr, stats) void
        +Swap(arr, i, j, stats) void
        -MergeSortRec(arr, l, r, stats) void
        -Merge(arr, l, m, r, stats) void
        -_quickSortRec(arr, l, r, strategy, stats) void
        -_partitioning(arr, l, r, pIdx, stats) int
    }

    Benchmark -- DataGenerator : gets data from
    Benchmark ..> SortUtils : calls sort functions
    DataGenerator -- TreatmentRecord : creates
    SortUtils -- TreatmentRecord : sorts
    SortUtils -- SortStats : updates
