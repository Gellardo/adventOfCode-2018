import common

def addr(op, reg):
    reg[op[3]] = reg[op[1]] + reg[op[2]]
    return reg
assert addr([0,1,2,3],[0,1,2,5]) == [0,1,2,3]

def addi(op, reg):
    reg[op[3]] = reg[op[1]] + op[2]
    return reg
assert addi([0,1,2,3],[0,1,0,5]) == [0,1,0,3]

def multr(op, reg):
    reg[op[3]] = reg[op[1]] * reg[op[2]]
    return reg
assert multr([0,1,2,3],[0,1,3,5]) == [0,1,3,3]

def multi(op, reg):
    reg[op[3]] = reg[op[1]] * op[2]
    return reg
assert multi([0,1,2,3],[0,1,3,5]) == [0,1,3,2]

def banr(op, reg):
    reg[op[3]] = reg[op[1]] & reg[op[2]]
    return reg
assert banr([0,1,2,3],[0,1,3,5]) == [0,1,3,1]

def bani(op, reg):
    reg[op[3]] = reg[op[1]] & op[2]
    return reg
assert bani([0,1,2,3],[0,1,3,5]) == [0,1,3,0]

def borr(op, reg):
    reg[op[3]] = reg[op[1]] | reg[op[2]]
    return reg
assert borr([0,1,2,3],[0,1,3,5]) == [0,1,3,3]

def bori(op, reg):
    reg[op[3]] = reg[op[1]] | op[2]
    return reg
assert bori([0,1,2,3],[0,1,3,5]) == [0,1,3,3]

def setr(op, reg):
    reg[op[3]] = reg[op[1]]
    return reg
assert setr([0,1,2,3],[0,1,3,5]) == [0,1,3,1]

def seti(op, reg):
    reg[op[3]] = op[1]
    return reg
assert seti([0,1,2,3],[0,1,3,5]) == [0,1,3,1]

def gtri(op, reg):
    reg[op[3]] = 1 if reg[op[1]] > op[2] else 0
    return reg
assert gtri([0,1,2,3],[0,1,3,5]) == [0,1,3,0]

def gtir(op, reg):
    reg[op[3]] = 1 if op[1] > reg[op[2]] else 0
    return reg
assert gtri([0,1,2,3],[0,1,3,5]) == [0,1,3,0]

def gtrr(op, reg):
    reg[op[3]] = 1 if reg[op[1]] > reg[op[2]] else 0
    return reg
assert gtri([0,1,2,3],[0,1,3,5]) == [0,1,3,0]

def eqri(op, reg):
    reg[op[3]] = 1 if reg[op[1]] == op[2] else 0
    return reg
assert gtri([0,1,2,3],[0,1,3,5]) == [0,1,3,0]

def eqir(op, reg):
    reg[op[3]] = 1 if op[1] == reg[op[2]] else 0
    return reg
assert gtri([0,1,2,3],[0,1,3,5]) == [0,1,3,0]

def eqrr(op, reg):
    reg[op[3]] = 1 if reg[op[1]] == reg[op[2]] else 0
    return reg
assert gtri([0,1,2,3],[0,1,3,5]) == [0,1,3,0]

opcodes = [
    addr,
    addi,
    multr,
    multi,
    banr,
    bani,
    borr,
    bori,
    setr,
    seti,
    gtri,
    gtir,
    gtrr,
    eqri,
    eqir,
    eqrr,
]

def test_opcodes(op, reg, result):
    return [opc(op, reg[:]) == result for opc in opcodes]

