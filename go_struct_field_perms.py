#!/usr/bin/env python3

import itertools
import sys
import tempfile
import os
import subprocess

go_program_head = '''
package main

import (
\t"fmt"
\t"unsafe"
)

func main() {
\tvar wordSize = unsafe.Sizeof(uintptr(0))
\tfmt.Printf("wordsize = %d\\n", wordSize)
\tvar n uintptr

'''

go_program_tail = r'''
}
'''


def main():
    fields = sys.argv[1:]
    if not fields:
        print('missing struct fields', file=sys.stderr)
        print(file=sys.stderr)
        print('usage: %s struct_fields' % (sys.argv[0],), file=sys.stderr)
        sys.exit(1)
    fd, filename = tempfile.mkstemp(prefix='go_struct_field_perms_', suffix='.go')
    print(filename, file=sys.stderr)
    try:
        with os.fdopen(fd, 'w') as f:
            f.write(go_program_head)
            for flds in itertools.permutations(fields):
                f.write(section(flds))
            f.write(go_program_tail)
        subprocess.run(['go', 'run', filename])
    finally:
        os.remove(filename)
    # print(section(['bool', 'int16', 'float64']))


def section(field_types):
    return (
            '\tn = unsafe.Sizeof(struct {\n' +
            ''.join("\t\tf" + str(i) + " " + s + "\n" for (i, s) in enumerate(field_types)) +
            '\t}{})\n' +
            '\tfmt.Printf("%16d bytes, %8d words => ' + ' '.join(field_types) + '\\n", n, n/wordSize)\n'
    )


if __name__ == '__main__':
    main()

# '''
# package main
#
# import (
# 	"fmt"
# 	"unsafe"
# )
#
# func main() {
# 	var wordSize = unsafe.Sizeof(uintptr(0))
# 	fmt.Printf("wordsize = %d\n", wordSize)
# 	var n uintptr
#
# 	n = unsafe.Sizeof(struct {
# 		bool
# 		float64
# 		int16
# 	}{})
# 	fmt.Printf("bool float64 int16 => %d bytes, %d words\n", n, n/wordSize) // a b c
#
# 	n = unsafe.Sizeof(struct {
# 		bool
# 		int16
# 		float64
# 	}{})
# 	fmt.Printf("bool int16 float64 => %d bytes, %d words\n", n, n/wordSize) // a c b
#
# 	n = unsafe.Sizeof(struct {
# 		float64
# 		bool
# 		int16
# 	}{})
# 	fmt.Printf("float64 bool int16 => %d bytes, %d words\n", n, n/wordSize) // b a c
#
# 	n = unsafe.Sizeof(struct {
# 		float64
# 		int16
# 		bool
# 	}{})
# 	fmt.Printf("float64 int16 bool => %d bytes, %d words\n", n, n/wordSize) // b c a
#
# 	n = unsafe.Sizeof(struct {
# 		int16
# 		bool
# 		float64
# 	}{})
# 	fmt.Printf("int16 bool float64 => %d bytes, %d words\n", n, n/wordSize) // c a b
#
# 	n = unsafe.Sizeof(struct {
# 		int16
# 		float64
# 		bool
# 	}{})
# 	fmt.Printf("int16 float64 bool => %d bytes, %d words\n", n, n/wordSize) // c b a
# }
# '''
