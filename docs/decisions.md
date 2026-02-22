# Engineering Decisions and Trade-offs

This document analyzes the key technical decisions made during the development of the CLI Task Manager and their associated trade-offs.

## Data Storage Approach

### Decision: JSON File Storage

**Chosen approach**: Local JSON file (`tasks.json`) with read-modify-write pattern.

**Trade-offs**:

| Aspect | JSON (Chosen) | SQLite (Alternative) | CSV (Alternative) |
|--------|---------------|---------------------|------------------|
| **Complexity** | Low - native Python support | Medium - SQL knowledge required | Low - limited structure |
| **Readability** | High - human-readable | Medium - requires queries | High - limited data types |
| **Performance** | Good for <1000 tasks | Better for large datasets | Good for simple data |
| **Data integrity** | Basic - no ACID | High - ACID compliant | Low - no schema |
| **Dependencies** | None | Built-in sqlite3 | None |

**Rationale**: For a single-user CLI tool with expected small datasets, JSON provides optimal simplicity without sacrificing functionality. The performance difference is negligible at this scale.

## CLI Parsing Strategy

### Decision: argparse vs Manual Parsing

**Chosen approach**: Python's built-in `argparse` module.

**Trade-offs**:

| Aspect | argparse (Chosen) | Manual parsing | Click/Typer (Third-party) |
|--------|-------------------|----------------|---------------------------|
| **Dependencies** | None | None | External |
| **Code volume** | Medium | Low initially, high later | Low |
| **Help generation** | Automatic | Manual implementation | Automatic |
| **Error handling** | Built-in | Manual implementation | Built-in |
| **Learning curve** | Medium | Low | Low |

**Rationale**: `argparse` provides professional CLI features without dependency overhead. The initial learning investment pays off in reduced boilerplate code for validation and help text.

## ID Management Strategy

### Decision: Sequential Integer IDs with Re-indexing

**Chosen approach**: Sequential IDs starting from 1, with re-indexing after deletions.

**Trade-offs**:

| Approach | Pros | Cons |
|----------|------|------|
| **Sequential with re-indexing** (Chosen) | User-friendly, predictable IDs, no gaps | O(n) delete operation |
| **Sequential without re-indexing** | O(1) delete, simple | Gaps in IDs, less intuitive |
| **UUIDs** | Globally unique, no collisions | Not user-friendly, long strings |
| **Timestamps** | Chronological ordering | Not user-friendly, potential collisions |

**Rationale**: User experience was prioritized. For small datasets, the O(n) re-indexing cost is negligible compared to the benefit of clean, memorable IDs.

## Error Handling Strategy

### Decision: Graceful Degradation with stderr Messages

**Chosen approach**: Boolean return values with stderr error messages.

**Trade-offs**:

| Approach | Pros | Cons |
|----------|------|------|
| **Boolean return + stderr** (Chosen) | Simple, Unix conventions, scriptable | Less structured than exceptions |
| **Exceptions** | Structured handling, stack traces | More verbose, may expose internals |
| **Exit codes only** | Unix-standard, scriptable | Less user-friendly interactively |
| **Logging framework** | Structured, configurable | Overkill for simple CLI |

**Rationale**: For a CLI tool, this approach balances user-friendliness with scriptability. Exceptions would be overkill for this use case.

## File I/O Pattern

### Decision: Read-Modify-Write Pattern

**Chosen approach**: Load entire file, modify in memory, write back completely.

**Trade-offs**:

| Approach | Pros | Cons |
|----------|------|------|
| **Read-modify-write** (Chosen) | Simple, atomic, consistent | Higher memory usage |
| **Append-only log** | Better performance, audit trail | Complex, requires compaction |
| **In-place modification** | Memory efficient | Risk of corruption |
| **Database** | ACID properties, concurrency | Overkill for this use case |

**Rationale**: Simplicity and data consistency were prioritized. Memory usage is acceptable for expected data volumes, and the approach ensures file validity.

## Architectural Approach

### Decision: Functional Design vs Object-Oriented

**Chosen approach**: Functional design with separate functions, no classes.

**Trade-offs**:

| Approach | Pros | Cons |
|----------|------|------|
| **Functional** (Chosen) | Simple, stateless, minimal overhead | No encapsulation, harder to extend |
| **Class-based** | Encapsulation, easier extension | More boilerplate, overkill |
| **Hybrid** | Balance of both | More complex design |

**Rationale**: The application's stateless operations and simple data flow make functional design ideal. Classes would add unnecessary complexity without providing clear benefits.

## Concurrency Considerations

### Decision: No Concurrency Control

**Chosen approach**: Single-threaded execution without file locking.

**Trade-offs**:

| Approach | Pros | Cons |
|----------|------|------|
| **No concurrency** (Chosen) | Simple, no locking overhead | Race conditions possible |
| **File locking** | Prevents corruption | Complex, platform-specific |
| **Database transactions** | ACID properties | Overkill, external dependency |

**Rationale**: For a single-user CLI tool, the probability of concurrent access is extremely low. The simplicity gained outweighs the theoretical risk of data corruption.

## Performance Implications

### Current Limitations

- **Search complexity**: O(n) linear search for all operations
- **Memory usage**: Loads entire dataset into memory
- **I/O pattern**: Full file rewrite on every change
- **Scalability**: Performance degrades with >10,000 tasks

### Scaling Thresholds

- **Small scale** (<100 tasks): Optimal performance
- **Medium scale** (100-1000 tasks): Acceptable performance
- **Large scale** (>1000 tasks): Noticeable degradation
- **Very large scale** (>10,000 tasks): Poor performance

**Rationale**: The design prioritizes simplicity over performance, which is appropriate for the expected use case of personal task management.
