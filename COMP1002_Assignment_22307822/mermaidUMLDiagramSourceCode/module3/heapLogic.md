```mermaid
flowchart TD
    A["Start extract_priority()"] --> B{"self.count == 0?"}
    B -- Yes --> C["Print EXTRACT FAILED"]
    C --> D["Return None"]
    B -- No --> E["Save root_request = heap_array[0]"]
    E --> F["self.count -= 1"]
    F --> G["Move last_element = heap_array[self.count] to heap_array[0]"]
    G --> H["call TrickleDown(0)"]
    J["call displayHeapArray()"] --> K["Return root_request"]