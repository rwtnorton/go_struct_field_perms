# go_struct_field_perms

Commandline utility to measure the size of different orderings of fields in Go structs.

## Usage

```
$ ./go_struct_field_perms.py bool float64 int16 |sort -n
wordsize = 8
              16 bytes,        2 words => bool int16 float64
              16 bytes,        2 words => float64 bool int16
              16 bytes,        2 words => float64 int16 bool
              16 bytes,        2 words => int16 bool float64
              24 bytes,        3 words => bool float64 int16
              24 bytes,        3 words => int16 float64 bool
```

More comlicated field types will likely need to be quoted
to avoid confusing your shell:
```
$ ./go_struct_field_perms.py '[7]bool' '*complex64' '[]string' 'struct { uintptr; rune }' |sort -n
wordsize = 8
              56 bytes,        7 words => *complex64 [7]bool []string struct { uintptr; rune }
              56 bytes,        7 words => *complex64 [7]bool struct { uintptr; rune } []string
              56 bytes,        7 words => *complex64 []string [7]bool struct { uintptr; rune }
              56 bytes,        7 words => *complex64 []string struct { uintptr; rune } [7]bool
              56 bytes,        7 words => *complex64 struct { uintptr; rune } [7]bool []string
              56 bytes,        7 words => *complex64 struct { uintptr; rune } []string [7]bool
              56 bytes,        7 words => [7]bool *complex64 []string struct { uintptr; rune }
              56 bytes,        7 words => [7]bool *complex64 struct { uintptr; rune } []string
              56 bytes,        7 words => [7]bool []string *complex64 struct { uintptr; rune }
              56 bytes,        7 words => [7]bool []string struct { uintptr; rune } *complex64
              56 bytes,        7 words => [7]bool struct { uintptr; rune } *complex64 []string
              56 bytes,        7 words => [7]bool struct { uintptr; rune } []string *complex64
              56 bytes,        7 words => []string *complex64 [7]bool struct { uintptr; rune }
              56 bytes,        7 words => []string *complex64 struct { uintptr; rune } [7]bool
              56 bytes,        7 words => []string [7]bool *complex64 struct { uintptr; rune }
              56 bytes,        7 words => []string [7]bool struct { uintptr; rune } *complex64
              56 bytes,        7 words => []string struct { uintptr; rune } *complex64 [7]bool
              56 bytes,        7 words => []string struct { uintptr; rune } [7]bool *complex64
              56 bytes,        7 words => struct { uintptr; rune } *complex64 [7]bool []string
              56 bytes,        7 words => struct { uintptr; rune } *complex64 []string [7]bool
              56 bytes,        7 words => struct { uintptr; rune } [7]bool *complex64 []string
              56 bytes,        7 words => struct { uintptr; rune } [7]bool []string *complex64
              56 bytes,        7 words => struct { uintptr; rune } []string *complex64 [7]bool
              56 bytes,        7 words => struct { uintptr; rune } []string [7]bool *complex64
```

## Prerequisites

- Python3
- Go

## Design

This is a Python script that writes a simple Go program to a temp file, enumerating
all permutations of the given struct field orderings, and then runs that
program via `go run`.  Temporary file should automatically be cleaned up.

## Caveats

No attempt is made to verify valid Go types are supplied as args.
Consequently, when `go run` executes, go will explode at runtime.

## Credits

This program follows directly from a desire to further explore the introduction
to `unsafe.Sizeof` in Chapter 13, Section 1 of "The Go Programming Language" 1st edition,
by Alan A. A. Donovan and Brian W. Kernighan.  A second reading of this classic
lead me to explore areas that I had only skimmed during a first reading.
