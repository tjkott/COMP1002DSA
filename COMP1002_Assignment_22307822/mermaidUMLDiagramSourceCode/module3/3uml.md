```mermaid
classDiagram
    direction RL

    class DSAEmergencyHeap {
        -heap_array : PriorityRequest[]
        -count : int
        +insert(patient_id, time, patient_table) void
        +peek() PriorityRequest
        +extract_priority() PriorityRequest
        -TrickleUp(index) void
        -TrickleDown(index) void
    }

    class PriorityRequest {
        +patient_id : int
        +treatment_time : int
        +priority_score : float
        +patient_name : string
        +patient_urgency : int
        +__str__() string
    }

    class DSAHashTable {
        -table : DSALinkedList[]
        +insert(record: PatientRecord) void
        +search(patient_id: int) PatientRecord
        +delete(patient_id: int) void
    }

    class DSALinkedList {
       +insertLast(value) void
       +removeByPatientId(patient_id) PatientRecord
    }

    class PatientRecord {
      +patient_id : int
      +name : string
      +age : int
      +department : string
      +urgency_level : int
      +treatment_status : string
    }

    DSAEmergencyHeap -- PriorityRequest : stores requests in array
    DSAEmergencyHeap ..> DSAHashTable : depends on (for patient lookup)
    DSAHashTable -- DSALinkedList : uses as chains
    DSALinkedList -- PatientRecord : stores records