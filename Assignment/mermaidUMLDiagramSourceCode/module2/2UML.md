```mermaid
classDiagram
    direction LR

    class DSAHashTable {
        -capacity : int
        -count : int
        -max_load_factor : float
        -table : DSALinkedList[]
        +insert(record: PatientRecord) void
        +search(patientID: int) PatientRecord
        +delete(patientID: int) void
        +getLoadFactor() float
        +displayTable() list~string~
        -Resize() void
        -Hash(key: int) int
        -FindNextPrime(start_val: int) int
    }

    class DSALinkedList {
        -head : DSAListNode
        -count : int
        +insertLast(value: PatientRecord) void
        +removeByPatientID(patient_id: int) PatientRecord
        +__iter__() iterator
        +__len__() int
    }

    class DSAListNode {
      +value : PatientRecord
      +next : DSAListNode
    }

    class PatientRecord {
      +patientID : int
      +name : string
      +age : int
      +department : string
      +urgencyLevel : int
      +treatmentStatus : string
      +__str__() string
    }

    DSAHashTable -- DSALinkedList : uses as chains
    DSALinkedList -- DSAListNode : contains
    DSAListNode -- PatientRecord : holds value
    DSALinkedList -- PatientRecord : stores
    DSAHashTable -- PatientRecord : manages
