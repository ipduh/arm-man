# arm-man
arm (Advanced RISC Machines) man(ual) pages
<br>
<br>
#### Install arm manual pages
  If, you just want the arm-man pages you
do not need to congigure or run the generator.
<br>
Just copy the contents of the ./arm-man-pages directory
into your local man-pages/man-section directory.
ie /usr/local/share/man/man7/
<br>
See install.sh

<br>
<br>
### Examples

##### arm-man-pages directory
The ./arm-main-pages directory contains instruction indexes <br>
and a man page for each instruction in the A32/T32 and A64 Instruction Sets <br>
of the Armv8-A v86A xml specification.

##### arm-man man
```
$ man ./arm-man-pages/arm.7
$ man arm
```

##### Armv8-A A32/T32 Instruction Set Index
```
$ man ./arm-man-pages/arm32.7
$ man arm32
$ man arm32 |grep add |grep sp
   arm32-add-sp-i     Add to SP (immediate).
   arm32-add-sp-r     Add to SP (register).
$ man arm32-add-sp-i
```

##### Armv8-A A64 Instruction Set Index
```
$ man ./arm-man-pages/arm64.7
$ man arm64
$ man arm64 |grep movz
  arm64-mov-movz                Move (wide immediate): an alias of MOVZ.
  arm64-movz                    Move wide with zero.
$ man arm64-movz
```

##### arm-man man
```
$ man ./arm-man-pages/arm.7
$ man arm
```

<br>
<br>

##### Arm86A_xml
Armv8-A v86A, the xml used to produce the man pages.

<br>
<br>

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


