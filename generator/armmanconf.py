#!/usr/bin/env python3


#ISA_A32 = './Arm86A_xml/ISA_A32/'
ISA_A32 = '../Arm86A_xml/ISA_A32/'
#ISA_A64 = './Arm86A_xml/ISA_A64/'
ISA_A64 = '../Arm86A_xml/ISA_A64/'

ARM_VERSION = '8'
ARM_ARCHITECTURE_PROFILE = 'A'
ARM_ARCHITECTURE_PROFILE_TXT = 'A, Application'
ARM_XML_VERSION = '86A'

A64 = 'A64'
A64_MAN_PREFIX = 'arm64-'
#A64_BASE = './Arm86A_xml/ISA_A64/index.xml'
A64_BASE = '../Arm86A_xml/ISA_A64/index.xml'
#A64_SVE = './Arm86A_xml/ISA_A64/sveindex.xml'
A64_SVE = '../Arm86A_xml/ISA_A64/sveindex.xml'
A64_FPSIMD = '../Arm86A_xml/ISA_A64/fpsimdindex.xml'

A32 = 'AArch32'
A32_MAN_PREFIX = 'arm32-'
#A32_BASE = './Arm86A_xml/ISA_A32/index.xml'
A32_BASE = '../Arm86A_xml/ISA_A32/index.xml'
#A32_FPSIMD = './Arm86A_xml/ISA_A32/fpsimdindex.xml'
A32_FPSIMD = '../Arm86A_xml/ISA_A32/fpsimdindex.xml'

# OUTPUT DIRECTORY
MAN = '../arm-man-pages/'

MAN_A32_INDEX_NAME = 'arm32'
MAN_A64_INDEX_NAME = 'arm64'
MAN_ARM_NAME = 'arm'
MAN_A32_INSTRUCTIONS = MAN + 'arm32/base/'
MAN_A32_INSTRUCTIONS_FPSIMD = MAN + 'arm32/fpsimd/'
MAN_A64_INSTRUCTIONS = MAN + 'arm64/base/'
MAN_A64_INSTRUCTIONS_FPSIMD = MAN + 'arm64/fpsimd/'
MAN_A64_INSTRUCTIONS_SVE = MAN + 'arm64/sve/'
MAN_SECTION = '7'
MAN_PAGE_SUFFIX = '.' + MAN_SECTION
MAN_A32_INDEX = MAN + MAN_A32_INDEX_NAME + MAN_PAGE_SUFFIX
MAN_A64_INDEX = MAN + MAN_A64_INDEX_NAME + MAN_PAGE_SUFFIX
MAN_ARM = MAN + MAN_ARM_NAME + MAN_PAGE_SUFFIX

ARMMAN_VERSION = '0.4'
ARMMAN_NAME = 'arm-man'
ARMAN_AUTH = 'g0, george@ipduh.com'
ARMAN_REPO = 'https://github.com/ipduh/arm-man'
