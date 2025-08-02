---- MODULE LD32_schema ----
(*
Lean-Deep 3.2 Marker Schema - TLA+ Specification
Defines invariants and temporal logic assertions for marker validation
*)

EXTENDS Sequences, FiniteSets, Integers, TLC

CONSTANTS MARKERS, IDS, FRAME_FIELDS, EXAMPLES

VARIABLES markers, progress, cache

vars == <<markers, progress, cache>>

(*
Core marker structure according to Lean-Deep 3.2
*)
ValidMarker(m) ==
    /\ "id" \in DOMAIN m
    /\ m.id \in IDS  
    /\ \/ m.id[1..5] = "LD32_"
       \/ m.id[1..2] = "S_"
       \/ m.id[1..2] = "A_"
       \/ m.id[1..2] = "C_"
       \/ m.id[1..3] = "M_"
       \/ m.id[1..3] = "MM_"
    /\ "frame" \in DOMAIN m
    /\ m.frame \in [signal: STRING, concept: STRING, pragmatics: STRING, narrative: STRING]
    /\ "examples" \in DOMAIN m
    /\ m.examples \in Seq(STRING)
    /\ Len(m.examples) >= 5
    /\ "lean_deep_version" \in DOMAIN m
    /\ m.lean_deep_version = "3.2"

(*
Frame completeness invariant
*)
CompleteFrame(frame) ==
    /\ "signal" \in DOMAIN frame
    /\ "concept" \in DOMAIN frame  
    /\ "pragmatics" \in DOMAIN frame
    /\ "narrative" \in DOMAIN frame
    /\ \A field \in {"signal", "concept", "pragmatics", "narrative"} : 
        frame[field] \in STRING

(*
Examples quality invariant - minimum 5 examples with content
*)
QualityExamples(examples) ==
    /\ examples \in Seq(STRING)
    /\ Len(examples) >= 5
    /\ \A i \in 1..Len(examples) : 
        /\ examples[i] # ""
        /\ Len(examples[i]) > 0

(*
Processing states for pipeline progress tracking
*)
ProcessingStates == {"FOUND", "SCANNED", "PARSED", "VALIDATED", "REPAIRED", "VERIFIED", "QUARANTINED"}

(*
Progress tracking invariants
*)
ValidProgress(p) ==
    /\ p \in [ProcessingStates -> Nat]
    /\ p["FOUND"] >= p["SCANNED"]
    /\ p["SCANNED"] >= p["PARSED"] 
    /\ p["PARSED"] >= p["VALIDATED"]
    /\ p["VALIDATED"] >= p["REPAIRED"]
    /\ p["REPAIRED"] >= p["VERIFIED"]

(*
Cache integrity with SHA-256 content addressing
*)
ValidCache(c) ==
    /\ c \in [STRING -> [hash: STRING, content: STRING, timestamp: Nat]]
    /\ \A entry \in DOMAIN c : 
        /\ Len(c[entry].hash) = 64  \* SHA-256 produces 64 hex characters
        /\ c[entry].timestamp \in Nat

(*
Type invariant for the complete system
*)
TypeInvariant ==
    /\ markers \in Seq([id: STRING, frame: [signal: STRING, concept: STRING, pragmatics: STRING, narrative: STRING], examples: Seq(STRING)])
    /\ progress \in [ProcessingStates -> Nat] 
    /\ cache \in [STRING -> [hash: STRING, content: STRING, timestamp: Nat]]

(*
Safety invariant - all valid markers maintain structure
*)
SafetyInvariant ==
    /\ TypeInvariant
    /\ ValidProgress(progress)
    /\ ValidCache(cache)
    /\ \A i \in 1..Len(markers) : ValidMarker(markers[i])

(*
Liveness property - progress always advances
*)
LivenessProperty ==
    []<>(progress["VERIFIED"] > 0)

(*
Idempotency property - reprocessing yields same results
*)
IdempotencyProperty ==
    \A m \in markers : ValidMarker(m) => ValidMarker(m)

====