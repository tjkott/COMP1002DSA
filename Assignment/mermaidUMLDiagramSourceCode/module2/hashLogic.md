```mermaid
flowchart TD
    A[Start insert record] --> B{getLoadFactor > max_load_factor?}
    B -->|Yes| C[call Resize]
    B -->|No| D
    C --> D[index = Hash record.patientID]
    D --> E[Get chain = self.table index]
    E --> F{For existing_record in chain}
    F -->|Yes, has next| G{existing.patientID == record.patientID?}
    G -->|Yes Duplicate| H[Update existing_record fields]
    H --> Z[End]
    G -->|No| F
    F -->|No, end of chain| I[chain.insertLast record]
    I --> J[self.count += 1]
    J --> Z