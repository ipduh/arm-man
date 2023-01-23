#!/usr/bin/env python3

# ARMMAN_VERSION = '0.4'
# ARMMAN_NAME = 'arm-man'
# ARMMAN_AUTH = 'g0, george@ipduh.com'
# ARMMAN_REPO = 'https://github.com/ipduh/arm-man'

import os
import sys
import re
import textwrap
import xml.etree.ElementTree as Et
from armmanconf import *

def draw_man(inst_xml, man_out=1):

    tree = Et.parse(inst_xml)
    root = tree.getiterator()
    roo = tree.getroot()
    name_diagram_asm = ''
    classes_intro = ''
    heading = '.SS '
    instruction_title = ''
    instruction_type = ''
    instruction_class = ''
    mnemonic = ''
    alias_mnemonic = ''
    prefix_diagram_lines = ' '
    description_p = ''
    explanations = ''
    processed_regdiagrams = 0

    for child in list(root):

        if child.tag == 'heading':
            if len(list(child)) > 0:
                for elm in list(child):
                    heading += elm.itertext
            else:
                heading += child.text

        if child.tag == 'instructionsection':
            if child.attrib.get('type'):
                instruction_type = child.attrib.get('type')
            if child.attrib.get('title'):
                instruction_title = child.attrib.get('title')
        if child.tag == 'docvars':
            for docvar in list(child):
                if docvar.attrib.get('key') == 'mnemonic':
                    mnemonic = docvar.attrib.get('value')
                if docvar.attrib.get('key') == 'instr-class':
                    instruction_class = docvar.attrib.get('value')
                if docvar.attrib.get('key') == 'alias_mnemonic':
                    alias_mnemonic = "{}".format(docvar.attrib.get('value'))

        if child.tag == 'desc':
            for elm in list(child):
                if elm.tag == 'brief':
                    txt = "".join(elm.itertext()).strip()
                    description_p += textwrap.fill(txt, 80, initial_indent=' ', subsequent_indent=' ')
                    description_p += '\n\n'
                if elm.tag == 'authored':
                    for elmchi in list(elm):
                        if elmchi.tag == 'para':
                            txt = "".join(elmchi.itertext()).strip()
                            description_p += textwrap.fill(txt, 80, initial_indent=' ', subsequent_indent=' ')
                            description_p += '\n\n'
                        if elmchi.tag == 'list':
                            description_p = proc_desc_list(list(elmchi), description_p)
                if elm.tag == 'description':
                    for delm in list(elm):
                        if delm.tag == 'para':
                            txt = "".join(delm.itertext()).strip()
                            description_p += textwrap.fill(txt, 80, initial_indent=' ', subsequent_indent=' ')
                            description_p += '\n\n'
                if elm.tag == 'status':
                    description_p += textwrap.fill("Status : {}".format(elm.text), 100, initial_indent=' ')
                    description_p += '\n\n'
                if elm.tag == 'predicated':
                    description_p += textwrap.fill("Predicated : {}\n".format(elm.text), 100, initial_indent=' ')
                    description_p += '\n\n'
                if elm.tag == 'takes_pred_movprfx':
                    description_p += textwrap.fill("takes_pred_movprfx : {}\n".format(elm.text), 100, initial_indent=' ')
                    description_p += '\n\n'
                if elm.tag == 'encodingnotes':
                    for elmchi in list(elm):
                        if elmchi.tag == 'para':
                            txt = "".join(elmchi.itertext()).strip()
                            description_p += textwrap.fill(txt, 80, initial_indent=' ', subsequent_indent=' ')
                            description_p += '\n\n'

        if child.tag == 'iclass':
            icl_name = child.attrib.get('name')
            icl_id = child.attrib.get('id')
            icl_no_encodings = child.attrib.get('no_encodings')
            icl_isa = child.attrib.get('isa')
            name_diagram_asm += ".SS {} - {}".format(icl_name, icl_isa)
            if icl_id != str(icl_name).lower():
                name_diagram_asm += " - {}".format(icl_id)
            name_diagram_asm += '\n'

        symbols_encodedin = {}
        symbols_txt = {}
        l_symbols = []
        encodedins = []
        table_cols = []
        if child.tag == 'explanations':
            for elm in list(child):
                if elm.tag == 'explanation':
                    this_symbol = ''
                    for expl in list(elm):
                        if expl.tag == 'symbol':
                            explanations += textwrap.fill("".join(expl.itertext()), 100, initial_indent=' ')
                            explanations += '\n'
                            l_symbols.append("".join(expl.itertext()))
                            this_symbol = expl.text
                        if expl.tag == 'account':
                            encodedin = expl.attrib.get('encodedin')
                            symbols_encodedin[this_symbol] = encodedin
                            encodedins.append(encodedin)
                            if encodedin:
                                explanations += textwrap.fill("Encoded in {}".format(encodedin), 80, initial_indent='  ', subsequent_indent='  ')
                                explanations += '\n'
                            for explchild in list(expl):
                                if explchild.tag == 'intro':
                                    this_txt = "".join(explchild.itertext()).strip()
                                    symbols_txt[this_symbol] = this_txt
                                    explanations += textwrap.fill(this_txt, 80, initial_indent='  ', subsequent_indent='  ')
                                    explanations += '\n\n'

                        if expl.tag == 'definition':
                            encodedin = expl.attrib.get('encodedin')
                            encodedins.append(encodedin)
                            symbols_encodedin[this_symbol] = encodedin
                            if encodedin:
                                explanations += textwrap.fill("Encoded in {}".format(encodedin), 80, initial_indent='  ', subsequent_indent='  ')
                                explanations += '\n'
                            for defchild in list(expl):
                                if defchild.tag == 'intro':
                                    this_txt = "".join(defchild.itertext()).strip()
                                    symbols_txt[this_symbol] = this_txt
                                    explanations += textwrap.fill(this_txt, 80, initial_indent='  ', subsequent_indent='  ')
                                    explanations += '\n\n'
                                if defchild.tag == 'table':
                                    explanations_table = True
                                    # if defchild.attrib.get('class') == 'valuetable':
                                    for tablelm in list(defchild):
                                        if tablelm.tag == 'tgroup':
                                            if tablelm.attrib.get('cols').isdigit():
                                                '''
                                                # some of the xml is broken here e.g. at_sys.xml
                                                for i in range(0, int(tablelm.attrib.get('cols'))):
                                                    table_cols.append([])
                                                '''
                                                pass
                                            for tgroupelm in list(tablelm):
                                                if tgroupelm.tag == 'thead':
                                                    for theadelm in list(tgroupelm):
                                                        if theadelm.tag == 'row':
                                                            col = 0
                                                            for rowelm in list(theadelm):
                                                                if rowelm.tag == 'entry':
                                                                    table_cols.append([])
                                                                    table_cols[col].append("".join(rowelm.itertext()))
                                                                    col += 1
                                                if tgroupelm.tag == 'tbody':
                                                    for tbodyelm in list(tgroupelm):
                                                        if tbodyelm.tag == 'row':
                                                            col = 0
                                                            for rowelm in list(tbodyelm):
                                                                if rowelm.attrib.get('class') == 'feature':
                                                                    if len(list(rowelm)) == 0:
                                                                        table_cols[col].append(' ')
                                                                        col += 1
                                                                    else:
                                                                        for arcvars in list(rowelm):
                                                                            if arcvars.tag == 'arch_variants':
                                                                                for arcvar in list(arcvars):
                                                                                    if arcvar.tag == 'arch_variant':
                                                                                        table_cols[col].append(arcvar.attrib.get('feature'))
                                                                                        col += 1
                                                                else:
                                                                    table_cols[col].append("".join(rowelm.itertext()))
                                                                    col += 1
                                    # longest col str
                                    col_lengths = []
                                    for col in table_cols:
                                        longest = 0
                                        for cell in col:
                                            if len(str(cell)) > longest:
                                                longest = len(cell)
                                        col_lengths.append(longest)

                                    for y in range(0, len(table_cols[0])):
                                        this_row = '  '
                                        for x in range(0, len(table_cols)):
                                            this_row += "{}".format(table_cols[x][y])
                                            if col_lengths[x] > len(table_cols[x][y]):
                                                this_row += (col_lengths[x] - len(table_cols[x][y])) * ' '
                                            this_row += ' '
                                        this_row += '\n'
                                        explanations += this_row
                                    explanations += '\n'
                                    # done with tables
                                    table_cols = []

                                if defchild.tag == 'after':
                                    explanations += textwrap.fill("".join(defchild.itertext()), 80, initial_indent='  ', subsequent_indent='  ')
                                    explanations += '\n\n'

        # header
        if child.tag == 'encoding':
            encoding_label = child.get('label')
            if encoding_label:
                name_diagram_asm += ".SS {}".format(encoding_label)
            bitdiffs = child.get('bitdiffs')
            if bitdiffs:
                name_diagram_asm += "({})".format(bitdiffs)
            name_diagram_asm += '\n'

        if child.tag == 'regdiagram' and child.attrib.get('form') == '16':
            processed_regdiagrams += 1
            exceptions, names, diagram = proc_16_regdiag(list(child))
            diagram = prefix(diagram, prefix_diagram_lines)
            name_diagram_asm += '\n'
            name_diagram_asm += diagram
            name_diagram_asm += '\n'

        # if child.tag == 'regdiagram' and (child.attrib.get('form') == '32' or child.attrib.get('form') == '16x2'):
        if child.tag == 'regdiagram' and child.attrib.get('form') == '32':
            processed_regdiagrams += 1
            exceptions, names, diagram = proc_32_regdiag(list(child))
            diagram = prefix(diagram, prefix_diagram_lines)
            name_diagram_asm += '\n'
            name_diagram_asm += diagram
            name_diagram_asm += '\n'

        if child.tag == 'regdiagram' and child.attrib.get('form') == '16x2':
            processed_regdiagrams += 1
            exceptions, names, diagram = proc_216_regdiag(list(child))
            diagram = prefix(diagram, prefix_diagram_lines)
            name_diagram_asm += '\n'
            name_diagram_asm += diagram
            name_diagram_asm += '\n'

        if child.tag == 'asmtemplate':
            name_diagram_asm += '\n'
            for asm_elm in list(child):
                name_diagram_asm += asm_elm.text
            name_diagram_asm += '\n'

        if child.tag == 'ps_section':
            pstxt = ''
            for tag in list(child):
                pstxt += "".join(tag.itertext()).strip()
            if pstxt:
                name_diagram_asm += "\n{}\n".format(pstxt)

        if child.tag == 'classesintro':
            for ci_elm in list(child):
                classes_intro += ci_elm.text.replace(':', ': ')

    man = '.nh\n'
    # man += ".TH \"{}\" \"7\" \" \"  \"{}({})\" \"{}\"\n".format(instruction_title, instruction_type, icl_isa, instruction_class)
    man += ".TH \"{}\" \"7\" \" \"  \"{}\" \"{}\"\n".format(instruction_title, instruction_type, instruction_class)

    if heading:
        man += heading
        man += '\n'

    if alias_mnemonic and mnemonic:
        man += " {} is an alias of {}\n\n".format(alias_mnemonic, mnemonic)

    man += description_p
    man += '\n'

    if classes_intro:
        man += classes_intro
        man += '\n'

    man += '\n'
    prefixed_name_diagram_asm = prefix(name_diagram_asm, ' ')
    man += prefixed_name_diagram_asm
    man += '\n'

    # Assembler Symbols
    explanations_table = True
    if len(explanations) < 2:
        explanations_table = False

    if explanations_table:
        man += ".SS Assembler Symbols\n\n"
        man += explanations
        man += '\n'
    else:
        expls = roo.findall('.//explanations')
        exp = ''
        if expls:
            for tag in expls:
                exp += "".join(tag.itertext())

            explanations = exp.splitlines()
            explanations_no_empties = filter(lambda x: not re.match(r'^\s*$', x), explanations)

            if exp:
                print(".SS Assembler Symbols")
                for l in explanations_no_empties:
                    man += l

    man += '\n'
    ps_operation_elms = roo.findall(".//ps[@secttype='Operation']")
    operation_section = ''
    if ps_operation_elms:
        man += ".SS Operation\n\n"
        for elm in ps_operation_elms:
            if elm.tag == 'ps':
                for elmchi in list(elm):
                    operation_section += prefix("".join(elmchi.itertext()), ' ')
        man += operation_section
        man += '\n'
    if alias_mnemonic and mnemonic:
        man += ".SS Operation\n\n"
        man += " The manual of {} gives pseudocode for {}.\n".format(mnemonic, alias_mnemonic)

    tags = roo.findall('.//operationalnotes')
    opnotes = ''
    if tags:
        man += "\n.SS Operational Notes\n\n"
        p_sem = re.compile(';{1, 1}')
        for tag in tags:
            this_opnote = "".join(tag.itertext())
            if len(this_opnote) > 80 and not p_sem.search(this_opnote):
                for elm in list(tag.getiterator()):
                    opnote = elm.text
                    if not opnote:
                        continue
                    opnote = re.sub(r'\s{2,}', '', opnote)
                    # if re.search(r':\s*$', opnote):
                    #    opnote += ' \n'
                    opnote = opnote.replace(':', ': ')
                    opnote = " {}\n".format(opnote)
                    opnotes += opnote
            else:
                opnotes += "".join(tag.itertext())
        man += opnotes

    if man_out == 1:
        print(man)
    else:
        with open(man_out, 'w') as of:
            of.write(man)

    return True


def proc_desc_list(nodes, desc_str):
    content_txt = ''
    for li in nodes:
        if li.tag == 'listitem':
            for lichi in list(li):
                content_txt = ''
                if lichi.tag == 'content':
                    if lichi.text:
                        content_txt = textwrap.fill(lichi.text, 80, initial_indent=' ', subsequent_indent=' ')
                        content_txt += '\n'
                    for ligrandchi in list(lichi):
                        if ligrandchi.tag == 'list':
                            desc_str += content_txt
                            desc_str = proc_desc_list(list(ligrandchi), desc_str)
                            break
                        else:
                            txt = "".join(lichi.itertext()).strip().replace(':', ': ').replace('.', '. ')
                            desc_str += textwrap.fill(txt, 80, initial_indent=' ', subsequent_indent=' ')
                            desc_str += '\n\n'
    desc_str += '\n'
    return desc_str


def prefix(input_str, line_prefix):
    out_str = ''
    for line in input_str.split('\n'):
        if line.startswith('.SS'):
            out_str += "{}\n".format(line)
        else:
            out_str += "{}{}\n".format(line_prefix, line)
    return out_str


def draw_ascii_table(instr_xml, verbose=False):
    # to test
    tree = Et.parse(instr_xml)
    root = tree.getiterator()
    regdiagrams_count = 0
    brief_description = ''
    isect_type = None
    title = None
    mnemonic = None
    instruction_class = None
    alias_mnemonic = ''
    long_description = ''

    for child in list(root):
        if child.tag == 'instructionsection':
            if child.attrib.get('type'):
                isect_type = child.attrib.get('type')
                title = child.attrib.get('title')
        if child.tag == 'docvars':
            for docvar in list(child):
                if docvar.attrib.get('key') == 'mnemonic':
                    mnemonic = docvar.attrib.get('value')
                if docvar.attrib.get('key') == 'instr-class':
                    instruction_class = docvar.attrib.get('value')
                if docvar.attrib.get('key') == 'alias_mnemonic':
                    alias_mnemonic = "({})".format(docvar.attrib.get('value'))
        if child.tag == 'brief':
            if len(list(child)) > 0:
                for para in list(child):
                    brief_description += para.text
            else:
                brief_description = child.text

        if child.tag == 'regdiagram':
            regdiagrams_count += 1

    if isect_type == 'instruction' or isect_type == 'alias':
        if verbose:
            print("{} : {}".format(instr_xml, title))
        pass
    else:
        return False

    processed_regdiagrams = 0

    for child in list(root):
        if child.tag == 'iclass':
            icl_name = child.attrib.get('name')
            icl_id = child.attrib.get('id')
            icl_no_encodings = child.attrib.get('no_encodings')
            icl_isa = child.attrib.get('isa')
            print("-_-_-_-")
            print(" name: {name}, id: {id}, encs: {no_enc},  isa: {isa},".format(
                name=icl_name,
                id=icl_id,
                no_enc=icl_no_encodings,
                isa=icl_isa
            ))

        if child.tag == 'regdiagram' and child.attrib.get('form') == '16':
            processed_regdiagrams += 1
            exceptions, names, diagram = proc_16_regdiag(list(child))

        if child.tag == 'regdiagram' and (child.attrib.get('form') == '32' or child.attrib.get('form') == '16x2'):
            processed_regdiagrams += 1
            exceptions, names, diagram = proc_32_regdiag(list(child))

        if child.tag == 'regdiagram':
            if not instruction_class:
                instruction_class = '_None_'

            regdiagram_type = child.attrib.get('form')
            print(regdiagram_type)
            print(long_description)
            print("{:10}, {:80}, {:12}, {:10}, {:8}, {}/{}, {}, {}".format(mnemonic, instr_xml,
                                                                           isect_type, alias_mnemonic,
                                                                           instruction_class, processed_regdiagrams,
                                                                           regdiagrams_count,
                                                                           brief_description))

            print("boxes: {}".format(names))

            if regdiagrams_count > processed_regdiagrams:
                continue
            if regdiagrams_count == processed_regdiagrams:
                return True

    return False


def proc_16_regdiag(nodes, size=16):
    #  <regdiagram form="16" psname="">
    #    <box hibit="31" width="4" settings="4">
    #      <c>1</c>
    #      <c>0</c>
    #      <c>1</c>
    #      <c>0</c>
    #    </box>
    #    <box hibit="27" name="SP" settings="1">
    #      <c>0</c>
    #    </box>
    #    <box hibit="26" width="3" name="Rd" usename="1">
    #      <c colspan="3"></c>
    #    </box>
    #    <box hibit="23" width="8" name="imm8" usename="1">
    #      <c colspan="8"></c>
    #    </box>
    #  </regdiagram>

    xtra_bit = ' '
    bits = []
    box_r_edges = [False for i in range(32)]
    bits_rep = [" " for i in range(65)]
    names = []
    exceptions = ''
    out_str = ''

    for box in nodes:
        if box.attrib.get('hibit'):
            if box.attrib.get('width'):
                low_box_bit = int(box.attrib.get('hibit')) - int(box.attrib.get('width')) + 1
                box_r_edges[low_box_bit] = True
            else:
                low_box_bit = int(box.attrib.get('hibit'))
                box_r_edges[low_box_bit] = True

            if box.attrib.get('name'):
                if box.attrib.get('constraint'):
                    name = "{}({})".format(box.attrib.get('name'), box.attrib.get('constraint'))
                else:
                    name = box.attrib.get('name')

                hibit = int(box.attrib.get('hibit'))
                lobit = low_box_bit
                names.append([name, hibit, lobit])

        for cell in list(box):
            bit = cell.text
            if cell.text != '1' and cell.text != '0' and cell.text is not None:
                exceptions += cell.text
                exceptions += ', '

            if not bit or cell.attrib.get('colspan'):
                if cell.attrib.get('colspan'):
                    bit_count = int(cell.attrib.get('colspan'))
                    for i in range(bit_count):
                        bits.append('.')
                else:
                    bits.append('.')
            else:
                if bit == '(1)':
                    bit = '1'
                if bit == '(0)':
                    bit = '0'

                bits.append(bit)

    if size < 32:
        # delta = 32 - size
        delta = 16
        for i in range(delta):
            bits.append(xtra_bit)

    bitrow_str = bitrow(bits_rep, bits, box_r_edges)
    if names[0][1] == 31:
        bitrow_str = '|' + bitrow_str[1:]
    # four_row_bit_index2(box_r_edges, bitrow_str)
    out_str += four_row_bit_index_f(box_r_edges, bitrow_str, 16)
    out_str += '\n'
    out_str += draw_all_name_pointers(names)
    out_str += '\n'
    out_str += draw_names3(names)
    out_str += '\n'

    return exceptions, names, out_str


def proc_32_regdiag(nodes):
    out_str = ''
    bits = []
    box_r_edges = [False for i in range(32)]
    bits_rep = [" " for i in range(65)]
    names = []
    exceptions = ''

    for box in nodes:
        if box.attrib.get('hibit'):
            if box.attrib.get('width'):
                low_box_bit = int(box.attrib.get('hibit')) - int(box.attrib.get('width')) + 1
                box_r_edges[low_box_bit] = True
            else:
                low_box_bit = int(box.attrib.get('hibit'))
                box_r_edges[low_box_bit] = True

            if box.attrib.get('name'):
                if box.attrib.get('constraint'):
                    name = "{}({})".format(box.attrib.get('name'), box.attrib.get('constraint'))
                else:
                    name = box.attrib.get('name')

                hibit = int(box.attrib.get('hibit'))
                lobit = low_box_bit
                names.append([name, hibit, lobit])

        for cell in list(box):
            bit = cell.text
            if cell.text != '1' and cell.text != '0' and cell.text is not None:
                exceptions += cell.text
                exceptions += ', '

            if not bit or cell.attrib.get('colspan'):
                if cell.attrib.get('colspan'):
                    bit_count = int(cell.attrib.get('colspan'))
                    for i in range(bit_count):
                        bits.append('.')
                else:
                    bits.append('.')
            else:
                if bit == '(1)':
                    bit = '1'
                if bit == '(0)':
                    bit = '0'

                bits.append(bit)

    bitrow_str = bitrow(bits_rep, bits, box_r_edges)
    if names[0][1] == 31:
        bitrow_str = '|' + bitrow_str[1:]
    out_str += four_row_bit_index(box_r_edges, bitrow_str)
    out_str += '\n'
    out_str += draw_all_name_pointers(names)
    out_str += '\n'
    out_str += draw_names3(names)
    out_str += '\n'

    return exceptions, names, out_str


def proc_216_regdiag(nodes):
    out_str = ''
    bits = []
    box_r_edges = [False for i in range(32)]
    bits_rep = [" " for i in range(65)]
    names = []
    exceptions = ''

    for box in nodes:
        if box.attrib.get('hibit'):
            if box.attrib.get('width'):
                low_box_bit = int(box.attrib.get('hibit')) - int(box.attrib.get('width')) + 1
                box_r_edges[low_box_bit] = True
            else:
                low_box_bit = int(box.attrib.get('hibit'))
                box_r_edges[low_box_bit] = True

            if box.attrib.get('name'):
                if box.attrib.get('constraint'):
                    name = "{}({})".format(box.attrib.get('name'), box.attrib.get('constraint'))
                else:
                    name = box.attrib.get('name')

                hibit = int(box.attrib.get('hibit'))
                lobit = low_box_bit
                names.append([name, hibit, lobit])

        for cell in list(box):
            bit = cell.text
            if cell.text != '1' and cell.text != '0' and cell.text is not None:
                exceptions += cell.text
                exceptions += ', '

            if not bit or cell.attrib.get('colspan'):
                if cell.attrib.get('colspan'):
                    bit_count = int(cell.attrib.get('colspan'))
                    for i in range(bit_count):
                        bits.append('.')
                else:
                    bits.append('.')
            else:
                if bit == '(1)':
                    bit = '1'
                if bit == '(0)':
                    bit = '0'

                bits.append(bit)

    bitrow_str = bitrow(bits_rep, bits, box_r_edges)
    if names[0][1] == 31:
        bitrow_str = '|' + bitrow_str[1:]
    out_str += four_row_bit_index_216(box_r_edges, bitrow_str)
    out_str += '\n'
    out_str += draw_all_name_pointers(names)
    out_str += '\n'
    out_str += draw_names3(names)
    out_str += '\n'

    return exceptions, names, out_str


def draw_name_row(names):
    hib = 1
    name_ptr = '|'
    # name_arrow = ' \-'
    # name_arrow = '|-'
    name_arrow = '`-'
    out_str = ''
    previous_spaces = 0
    n = 0
    large_names = []
    for name in names:
        previous_name = ''
        if len(names) > 1 and n > 0:
            previous_name = names[(n-1)][0]

        spaces = (32 - name[hib] - 1)*2 - previous_spaces
        nl = len(previous_name)
        if (nl + len(name_arrow)) <= spaces and len(previous_name) > 0:
            out_str = out_str[:-1]
            out_str += name_arrow
            spaces_str = previous_name + (spaces - nl - len(name_arrow) + 1) * ' '
            out_str = out_str + spaces_str + name_ptr
            previous_spaces = len(out_str)
        else:
            spaces_str = spaces * ' '
            out_str = out_str + spaces_str + name_ptr
            if len(previous_name) > 0:
                large_names.append(names[n-1])
            previous_spaces = len(out_str)
        if n == len(names) - 1:
            out_str = out_str[:-1]
            out_str = out_str + name_arrow + name[0]
        n += 1

    out_str = out_str + os.linesep
    return out_str, large_names


def draw_names2(names):
    hib = 1
    name_arrow = '`-'
    name_ptr = '|'
    out_str, large_names = draw_name_row(names)
    while len(large_names) > 0:
        n = 0
        previous_spaces = 0
        this_str = ''
        for name in large_names:
            spaces = (32 - name[hib] - 1) * 2 - previous_spaces
            spaces_str = spaces * ' '
            this_str = this_str + spaces_str + name_ptr
            previous_spaces = len(this_str)
            if n == len(large_names) - 1:
                # this_str = this_str + name[0]
                this_str = this_str[:-1]
                this_str = this_str + name_arrow + name[0]
                large_names.remove(name)
            n += 1
        this_str += '\n'
        out_str += this_str
    return out_str


def draw_names3(names):
    out_str, large_names = draw_name_row(names)
    while len(large_names) > 0:
        this_str, large_names = draw_name_row(large_names)
        out_str += this_str
    return out_str


def draw_names(names):
    out_str = ''
    hib = 1
    name_ptr = '|'
    # name_arrow = ' \-'
    # name_arrow = '|-'
    name_arrow = '`-'
    this_str = ''
    previous_spaces = 0
    n = 0
    large_names = []
    for name in names:
        previous_name = ''
        if len(names) > 1 and n > 0:
            previous_name = names[(n-1)][0]

        spaces = (32 - name[hib] - 1)*2 - previous_spaces
        nl = len(previous_name)
        if (nl + len(name_arrow)) <= spaces and len(previous_name) > 0:
            this_str = this_str[:-1]
            this_str += name_arrow
            spaces_str = previous_name + (spaces - nl - len(name_arrow) + 1) * ' '
            this_str = this_str + spaces_str + name_ptr
            previous_spaces = len(this_str)
        else:
            spaces_str = spaces * ' '
            this_str = this_str + spaces_str + name_ptr
            if len(previous_name) > 0:
                large_names.append(names[n-1])
            previous_spaces = len(this_str)
        if n == len(names) - 1:
            this_str = this_str[:-1]
            this_str = this_str + name_arrow + name[0]
        n += 1

    this_str = this_str + os.linesep
    out_str += this_str

    while len(large_names) > 0:
        n = 0
        previous_spaces = 0
        this_str = ''
        for name in large_names:
            spaces = (32 - name[hib] - 1) * 2 - previous_spaces
            spaces_str = spaces * ' '
            this_str = this_str + spaces_str + name_ptr
            previous_spaces = len(this_str)
            if n == len(large_names) - 1:
                # this_str += name[0]
                this_str = this_str[:-1]
                this_str = this_str + name_arrow + name[0]
                large_names.remove(name)
            n += 1

        this_str += '\n'
        out_str += this_str

    return out_str


def draw_names_one_per_line(names):
    hib = 1
    name_ptr = '|'
    name_last_ptr = '\_'
    # name_last_ptr = ' \-'

    for i in range(len(names), -1, -1):
        this_str = ''
        previous_spaces = 0
        n = 0
        for name in names:
            n += 1
            if n < i:
                spaces = (32 - name[hib] - 1)*2 - previous_spaces
                spaces_str = spaces * ' '
                this_str = this_str + spaces_str + name_ptr
                previous_spaces = len(this_str)
            if n == i:
                spaces = (32 - name[hib] - 1)*2 - previous_spaces
                spaces_str = spaces * ' '
                this_str = this_str + spaces_str + name_last_ptr
                this_str += name[0]

        print(this_str)


def draw_all_name_pointers(names):
    hib = 1
    name_ptr = '|'

    this_str = ''
    previous_spaces = 0
    for name in names:
        spaces = (32 - name[hib] - 1)*2 - previous_spaces
        spaces_str = spaces * ' '
        this_str = this_str + spaces_str + name_ptr
        previous_spaces = len(this_str)

    return this_str


def bitrow(bits_rep, bits, box_r_edges):

    bits.reverse()
    for i in range(32):
        bits_rep[(i*2+1)] = bits[i]

    for i in range(32):
        if box_r_edges[i]:
            bits_rep[(2*i)] = '|'

    this_bitrow = bits_rep
    this_bitrow.reverse()
    bitrow_str = "".join(this_bitrow)

    return bitrow_str


def box_ptr(box_r_edges):
    str_ = [" " for i in range(65)]
    for i in range(32):
        if box_r_edges[i]:
            str_[(2*i)] = '|'

    str_.reverse()
    return "".join(str_)


def place_bit_index_ff(bit_nums_rep_row, index, offset):
    printed_index = index - offset
    if index < 10:
        bit_nums_rep_row[2*index] = str(printed_index)
    else:
        digit_1 = printed_index // 10
        digit_2 = printed_index % 10
        bit_nums_rep_row[2*index] = str(digit_2)
        bit_nums_rep_row[2*index + 1] = str(digit_1)


def place_bit_index_f(bit_nums_rep_row, index, offset):
    printed_index = index - offset
    if printed_index < 10:
        bit_nums_rep_row[2*index] = str(printed_index)
    else:
        digit_1 = printed_index // 10
        digit_2 = printed_index % 10
        bit_nums_rep_row[2*index] = str(digit_2)
        bit_nums_rep_row[2*index + 1] = str(digit_1)


def place_bit_index(bit_nums_rep_row, index):
    if index < 10:
        bit_nums_rep_row[2*index] = str(index)
    else:
        digit_1 = index // 10
        digit_2 = index % 10
        bit_nums_rep_row[2*index] = str(digit_2)
        bit_nums_rep_row[2*index + 1] = str(digit_1)


def four_row_bit_index(box_r_edges, bitrow_str):
    bit_nums0_rep = [" " for i in range(65)]
    bit_nums1_rep = [" " for i in range(65)]
    bit_nums2_rep = [" " for i in range(65)]
    bit_nums3_rep = [" " for i in range(65)]
    top = 0
    lob = 2
    for i in range(31, -1, -1):
        if box_r_edges[i]:
            if i < 30 and i > 9:
                if i < 29 and box_r_edges[i+3] and box_r_edges[i+2] and box_r_edges[i+1] and top == 3:
                    bit_nums0_rep[2 * i] = '|'
                    bit_nums1_rep[2 * i] = '|'
                    bit_nums2_rep[2 * i] = '|'
                    place_bit_index(bit_nums3_rep, i)
                    top = 4
                    continue
                if box_r_edges[i+2] and box_r_edges[i+1] and top == 2:
                    bit_nums0_rep[2 * i] = '|'
                    bit_nums1_rep[2 * i] = '|'
                    place_bit_index(bit_nums2_rep, i)
                    top = 3
                elif box_r_edges[i+1] and top == 1:
                    bit_nums0_rep[2 * i] = '|'
                    place_bit_index(bit_nums1_rep, i)
                    top = 2
                else:
                    place_bit_index(bit_nums0_rep, i)
                    top = 1
            elif i < 10:
                place_bit_index(bit_nums0_rep, i)
            elif i == 31 or i == 30:
                if i == 30 and box_r_edges[i+1]:
                    bit_nums0_rep[2 * i] = '|'
                    place_bit_index(bit_nums1_rep, i)
                    top = 2
                else:
                    place_bit_index(bit_nums0_rep, i)
                    top = 1

    bit_nums0_rep.reverse()
    bit_nums1_rep.reverse()
    bit_nums2_rep.reverse()
    bit_nums3_rep.reverse()
    out_str = "".join(bit_nums3_rep)
    out_str += '\n'
    out_str += "".join(bit_nums2_rep)
    out_str += '\n'
    out_str += "".join(bit_nums1_rep)
    out_str += '\n'
    out_str += "".join(bit_nums0_rep)
    out_str += '\n'
    out_str += box_ptr(box_r_edges)
    out_str += '\n'
    out_str += bitrow_str

    return out_str


def place_bit_index_216(bit_nums_rep_row, index):
    if index < 10:
        bit_nums_rep_row[2*index] = str(index)
    elif index < 16:
        digit_1 = index // 10
        digit_2 = index % 10
        bit_nums_rep_row[2*index] = str(digit_2)
        bit_nums_rep_row[2*index + 1] = str(digit_1)
    elif index > 15:
        d0 = index - 15
        digit_1 = d0 // 10
        digit_2 = d0 % 10
        bit_nums_rep_row[2*index] = str(digit_2)
        bit_nums_rep_row[2*index + 1] = str(digit_1)


def four_row_bit_index_216(box_r_edges, bitrow_str):
    bit_nums0_rep = [" " for i in range(65)]
    bit_nums1_rep = [" " for i in range(65)]
    bit_nums2_rep = [" " for i in range(65)]
    bit_nums3_rep = [" " for i in range(65)]
    top = 0
    lob = 2
    for i in range(31, -1, -1):
        if box_r_edges[i]:
            if i < 30 and i > 9:
                if i < 29 and box_r_edges[i+3] and box_r_edges[i+2] and box_r_edges[i+1] and top == 3:
                    bit_nums0_rep[2 * i] = '|'
                    bit_nums1_rep[2 * i] = '|'
                    bit_nums2_rep[2 * i] = '|'
                    place_bit_index_216(bit_nums3_rep, i)
                    top = 4
                    continue
                if box_r_edges[i+2] and box_r_edges[i+1] and top == 2:
                    bit_nums0_rep[2 * i] = '|'
                    bit_nums1_rep[2 * i] = '|'
                    place_bit_index_216(bit_nums2_rep, i)
                    top = 3
                elif box_r_edges[i+1] and top == 1:
                    bit_nums0_rep[2 * i] = '|'
                    place_bit_index_216(bit_nums1_rep, i)
                    top = 2
                else:
                    place_bit_index_216(bit_nums0_rep, i)
                    top = 1
            elif i < 10:
                place_bit_index_216(bit_nums0_rep, i)
            elif i == 31 or i == 30:
                if i == 30 and box_r_edges[i+1]:
                    bit_nums0_rep[2 * i] = '|'
                    place_bit_index_216(bit_nums1_rep, i)
                    top = 2
                else:
                    place_bit_index_216(bit_nums0_rep, i)
                    top = 1

    bit_nums0_rep.reverse()
    bit_nums1_rep.reverse()
    bit_nums2_rep.reverse()
    bit_nums3_rep.reverse()
    out_str = "".join(bit_nums3_rep)
    out_str += '\n'
    out_str += "".join(bit_nums2_rep)
    out_str += '\n'
    out_str += "".join(bit_nums1_rep)
    out_str += '\n'
    out_str += "".join(bit_nums0_rep)
    out_str += '\n'
    out_str += box_ptr(box_r_edges)
    out_str += '\n'
    out_str += bitrow_str

    return out_str


def four_row_bit_index_f(box_r_edges, bitrow_str, offset=16):
    bit_nums0_rep = [" " for i in range(65)]
    bit_nums1_rep = [" " for i in range(65)]
    bit_nums2_rep = [" " for i in range(65)]
    bit_nums3_rep = [" " for i in range(65)]
    top = 0
    for i in range(31, -1, -1):
        if box_r_edges[i]:
            if i < 30 and i > 9:
                if i < 29 and box_r_edges[i+3] and box_r_edges[i+2] and box_r_edges[i+1] and top == 3:
                    bit_nums0_rep[2 * i] = '|'
                    bit_nums1_rep[2 * i] = '|'
                    bit_nums2_rep[2 * i] = '|'
                    place_bit_index_f(bit_nums3_rep, i, offset)
                    top = 4
                    continue
                if box_r_edges[i+2] and box_r_edges[i+1] and top == 2:
                    bit_nums0_rep[2 * i] = '|'
                    bit_nums1_rep[2 * i] = '|'
                    place_bit_index_f(bit_nums2_rep, i, offset)
                    top = 3
                elif box_r_edges[i+1] and top == 1:
                    bit_nums0_rep[2 * i] = '|'
                    place_bit_index_f(bit_nums1_rep, i, offset)
                    top = 2
                else:
                    place_bit_index_f(bit_nums0_rep, i, offset)
                    top = 1
            elif i < 10:
                place_bit_index_f(bit_nums0_rep, i, offset)
            elif i == 31 or i == 30:
                if i == 30 and box_r_edges[i+1]:
                    bit_nums0_rep[2 * i] = '|'
                    place_bit_index_f(bit_nums1_rep, i, offset)
                    top = 2
                else:
                    place_bit_index_f(bit_nums0_rep, i, offset)
                    top = 1

    bit_nums0_rep.reverse()
    bit_nums1_rep.reverse()
    bit_nums2_rep.reverse()
    bit_nums3_rep.reverse()
    out_str = "".join(bit_nums3_rep)
    out_str += '\n'
    out_str += "".join(bit_nums2_rep)
    out_str += '\n'
    out_str += "".join(bit_nums1_rep)
    out_str += '\n'
    out_str += "".join(bit_nums0_rep)
    out_str += '\n'
    out_str += box_ptr(box_r_edges)
    out_str += '\n'
    out_str += bitrow_str

    return out_str


def version():
    print(VERSION)


if __name__ == '__main__':

    if not draw_man(sys.argv[1]):
        print("-) unable to produce man for {}".format(sys.argv[1]))

