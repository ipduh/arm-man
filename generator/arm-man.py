#!/usr/bin/env python3

ARMMAN_VERSION = '0.4'
ARMMAN_NAME = 'arm-man'
ARMMAN_AUTH = 'g0, george@ipduh.com'
ARMMAN_REPO = 'https://github.com/ipduh/arm-man'

from armmanconf import *
import armxmlproc
import xml.etree.ElementTree as Et
import os


def about_man(out_man_file):
    arm_va = "Arm{}-{}".format(ARM_VERSION, ARM_ARCHITECTURE_PROFILE)
    arm = ".\"Generator {} v{}, {}\n".format(ARMMAN_NAME, ARMMAN_VERSION, ARMMAN_REPO)
    arm = ".nh\n"
    #arm += ".TH \"Armv{}-{}\" \"7\"\n\n".format(ARM_VERSION, ARM_ARCHITECTURE_PROFILE)
    arm += ".TH \"Armv{}-{}\" \"7\" \"\" \"\" \"arm man man\"  \n\n".format(ARM_VERSION, ARM_ARCHITECTURE_PROFILE)
    arm += ".SS Arm Version\n"
    arm += " {}\n\n".format(ARM_VERSION)
    arm += ".SS Arm Architecture Profile\n"
    arm += " {}\n\n".format(ARM_ARCHITECTURE_PROFILE_TXT)
    arm += ".SS Arm specification xml Version\n"
    arm += " {}\n\n".format(ARM_XML_VERSION)
    arm += ".SS {} A32/T32 Instruction Set Index\n".format(arm_va)
    arm += " man {}\n\n".format(MAN_A32_INDEX_NAME)
    arm += ".SS {} A32/T32 instruction man prefix\n".format(arm_va)
    arm += " {}\n\n".format(A32_MAN_PREFIX)
    arm += ".SS {} A64 Instruction Set Index\n".format(arm_va)
    arm += " man {}\n\n".format(MAN_A64_INDEX_NAME)
    arm += ".SS {} A64 instruction man prefix\n".format(arm_va)
    arm += " {}\n\n".format(A64_MAN_PREFIX)
    arm += ".SS {} Examples \n".format(arm_va)

    with open(out_man_file, 'w') as of:
        of.write(arm)


def all_a64_man(outfile, outinstrdir=0):
    prefix = A64_MAN_PREFIX
    base_instruction_set, base_title, base_instructions = proc_index(A64_BASE)
    fpsimd_instruction_set, fpsimd_title, fpsimd_instructions = proc_index(A64_FPSIMD)
    sve_instruction_set, sve_title, sve_instructions = proc_index(A64_SVE)

    if not os.path.exists(MAN_A64_INSTRUCTIONS):
        os.makedirs(MAN_A64_INSTRUCTIONS, exist_ok=True)
    if not os.path.exists(MAN_A64_INSTRUCTIONS_FPSIMD):
        os.mkdir(MAN_A64_INSTRUCTIONS_FPSIMD)
    if not os.path.exists(MAN_A64_INSTRUCTIONS_SVE):
        os.mkdir(MAN_A64_INSTRUCTIONS_SVE)

    if not outinstrdir == 0:
        create_manuals(base_instructions, ISA_A64, MAN_A64_INSTRUCTIONS, prefix)
        print("+) {} : {}".format(base_title, len(base_instructions)))
        create_manuals(fpsimd_instructions, ISA_A64, MAN_A64_INSTRUCTIONS_FPSIMD, prefix)
        print("+) {} : {}".format(fpsimd_title, len(fpsimd_instructions)))
        create_manuals(sve_instructions, ISA_A64, MAN_A64_INSTRUCTIONS_SVE, prefix)
        print("+) {} : {}".format(sve_title, len(sve_instructions)))

    out = ".nh\n"
    out += ".TH \"{}\" \"7\" \" \"  \"{}\" \"{}\"\n".format('A64-Instructions', ' ', ' ')
    if base_instruction_set == A64:
        out += ".SS {}\n".format(base_title)
        out += to_man_short(base_instructions, prefix)
        out += " \n"
    if fpsimd_instruction_set == A64:
        out += ".SS {}\n".format(fpsimd_title)
        out += to_man_short(fpsimd_instructions, prefix)
        out += " \n"
    if sve_instruction_set == A64:
        out += ".SS {}\n".format(sve_title)
        out += to_man_short(sve_instructions, prefix)
        out += " \n"

    with open(outfile, 'w') as of:
        of.write(out)

    return True


def all_a32_man(outindex, outinstdir=0):

    prefix = A32_MAN_PREFIX
    base_instruction_set, base_title, base_instructions = proc_index(A32_BASE)
    fpsimd_instruction_set, fpsimd_title, fpsimd_instructions = proc_index(A32_FPSIMD)

    if not os.path.exists(MAN_A32_INSTRUCTIONS):
        os.makedirs(MAN_A32_INSTRUCTIONS, exist_ok=True)
    if not os.path.exists(MAN_A32_INSTRUCTIONS_FPSIMD):
        os.mkdir(MAN_A32_INSTRUCTIONS_FPSIMD)

    if not outinstdir == 0:
        create_manuals(base_instructions, ISA_A32, MAN_A32_INSTRUCTIONS, prefix)
        print("+) {} : {}".format(base_title, len(base_instructions)))
        create_manuals(fpsimd_instructions, ISA_A32, MAN_A32_INSTRUCTIONS_FPSIMD, prefix)
        print("+) {} : {}".format(fpsimd_title, len(fpsimd_instructions)))

    out = ".nh\n"
    out += ".TH \"{}\" \"7\" \" \"  \"{}\" \"{}\"\n".format('AArch32-Instructions', ' ', ' ')
    if base_instruction_set == A32:
        out += ".SS {}\n".format(base_title)
        out += to_man_short(base_instructions, prefix)
        out += " \n"
    if fpsimd_instruction_set == A32:
        out += ".SS {}\n".format(fpsimd_title)
        out += to_man_short(fpsimd_instructions, prefix)
        out += " \n"
    with open(outindex, 'w') as of:
        of.write(out)

    return True


def create_manuals(instructions, isa_dir, man_dir, prefix, verbose=False):
    aOKs = 0
    for instr in instructions:
        xml = isa_dir + instr + '.xml'
        man = man_dir + prefix + instr.replace('_', '-') + MAN_PAGE_SUFFIX
        status = False
        if verbose:
            print("+) Processing {}".format(instr))
        if os.path.exists(xml):
            status = armxmlproc.draw_man(xml, man)
            if not status:
                print("+) error in {} while processing {}".format(man, xml))
            else:
                aOKs += 1
        else:
            print("+) {} does not exist.".format(xml))

    return True


def one_index_one_man(input_xml, outfile):

    instruction_set, title, instructions = proc_index(input_xml)
    prefix = ''
    if instruction_set == 'A32':
        prefix = A32_MAN_PREFIX
    if instruction_set == 'A64':
        prefix = A64_MAN_PREFIX

    out = '.nh\n'
    out += ".TH \"{}\" \"7\" \" \"  \"{}\" \"{}\"\n".format(instruction_set, ' ', ' ')
    out += ".SS {}\n".format(title)
    out += to_man_short(instructions, prefix)

    with open(outfile, 'w') as of:
        of.write(out)


def proc_index(input_xml):

    tree = Et.parse(input_xml)
    #root = tree.getiterator()
    root = tree.getiterator()
    instruction_set = ''
    the_title = ''
    instructions = {}

    for elm in list(root):
        if elm.tag == 'alphaindex':
            pass
        if elm.tag == 'toptitle':
            instruction_set = elm.attrib.get('instructionset')

        if elm.tag == 'iforms':
            the_title = elm.attrib.get('title')
            for elmchi in list(elm):
                if elmchi.tag == 'iform':
                    this_id = elmchi.attrib.get('id')
                    if this_id:
                        this_id = this_id.lower()
                        instructions[this_id] = elmchi.text

    return instruction_set, the_title, instructions


def to_man_short(instructions, prefix=''):
    instrs = {}
    for i, t in instructions.items():
        this_key = prefix + i.lower().replace('_', '-')
        instrs[this_key] = t

    longest_instruction = 'X'
    longest_description = 'x'
    for i, t in instrs.items():
        if len(i) > len(longest_instruction):
            longest_instruction = i
        if len(t) > len(longest_description):
            longest_description = t

    out = ''
    for i, t in instrs.items():
        out += ' '
        out += i.replace('_', '-')
        out += (len(longest_instruction) - len(i)) * ' '
        out += '  '
        out += t
        out += (len(longest_description) - len(t)) * ' '
        out += '\n'

    return out


def all_man():

    if not os.path.exists(MAN):
        os.mkdir(MAN)

    print(")) {} v{}, {}\n".format(ARMMAN_NAME, ARMMAN_VERSION, ARMMAN_REPO))
    about_man(MAN_ARM)
    all_a32_man(MAN_A32_INDEX, MAN_A32_INSTRUCTIONS)
    print("+) ARM AArch32 instruction index and man pages generated.\n")
    all_a64_man(MAN_A64_INDEX, MAN_A32_INSTRUCTIONS)
    print("+) ARM A64 instruction index and man pages generated.\n")
    print(")) ARM man pages in {}".format(MAN))
    exit(0)

if __name__ == '__main__':
    all_man()
