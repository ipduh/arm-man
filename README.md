# arm-man
arm (Advanced RISC Machines) man(ual) pages

**arm-man-pages**
A man page for each instruction in the A32/T32 and A64 Instruction Sets
in the Armv8-A v86A xml specification.

arm.7  , arm-man man
arm32.7, The A32/T32 Instruction set index
arm64.7, The A64 Instruction set index

**Arm86A_xml**
Armv8-A v86A, the xml used to produce the man pages.

##### Install arm manual pages
  If, you just want the arm-man pages you
do not need to congigure or run the generator.
Just copy the contents of the ./arm-man-pages directory
into your local man-pages/man-section directory.
ie /usr/local/share/man/man7/
See install.sh

##### Man Info
```
$ man ./arm-man-pages/arm.7
$ man arm
```

##### Armv8-A A32/T32 Instruction Set Index
```
$ man ./arm-man-pages/arm32.7
$ man arm32
```

##### Armv8-A A64 Instruction Set Index
```
$ man ./arm-man-pages/arm64.7
$ man arm64
```

##### Generate man pages from the spec xml.
```
$ cd generator
$ ./arm-man.py
)) arm-man v0.4, https://github.com/ipduh/arm-man

+) AArch32 -- Base Instructions (alphabetic order) : 301
+) AArch32 -- SIMD&FP Instructions (alphabetic order) : 266
+) ARM AArch32 instruction index and man pages generated.

+) A64 -- Base Instructions (alphabetic order) : 348
+) A64 -- SIMD and Floating-point Instructions (alphabetic order) : 404
+) A64 -- SVE Instructions (alphabetic order) : 508
+) ARM A64 instruction index and man pages generated.

)) ARM man pages in ../arm-man-pages/

```

