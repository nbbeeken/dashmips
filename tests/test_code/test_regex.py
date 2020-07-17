"""Test regular expressions for every instruction."""
import re
from dashmips.instructions import Instructions


def test_add():
    """Test the add instruction."""
    add_regex = Instructions["add"].regex
    assert re.match(add_regex, "add $t0, $t1, $t2") is not None
    assert re.match(add_regex, "add $t0, $zero, $t2") is not None
    assert re.match(add_regex, "add $t0, hi, lo") is None  # hi lo are non accessible registers


def test_addi():
    """Test the addi instruction."""
    addi_regex = Instructions["addi"].regex
    assert re.match(addi_regex, "addi $t0, $t1, 1") is not None
    assert re.match(addi_regex, "addi $t0, $zero, 1") is not None
    assert re.match(addi_regex, "addi $t0, $t1, $zero") is None
    assert re.match(addi_regex, "addi $t0, hi, 1") is None


def test_sub():
    """Test the sub instruction."""
    sub_regex = Instructions["sub"].regex
    assert re.match(sub_regex, "sub $t0, $t1, $t2") is not None
    assert re.match(sub_regex, "sub $t0, $zero, $t2") is not None
    assert re.match(sub_regex, "sub $t0, hi, lo") is None


def test_lw():
    """Test the lw instruction."""
    lw_regex = Instructions["lw"].regex
    assert re.match(lw_regex, "lw $t1, 0($t1)") is not None
    assert re.match(lw_regex, "lw $t0, $t1") is None
    assert re.match(lw_regex, "lw $zero, 0($t1)") is not None


def test_sw():
    """Test the sw instruction."""
    sw_regex = Instructions["sw"].regex
    assert re.match(sw_regex, "sw $t1, 0($t1)") is not None
    assert re.match(sw_regex, "sw $t0, $t1") is None
    assert re.match(sw_regex, "sw $zero, 0($t1)") is not None


def test_la():
    """Test the la instruction."""
    la_regex = Instructions["la"].regex
    assert re.match(la_regex, "la $t1, argc_str") is not None
    assert re.match(la_regex, "la $t1, $t0") is None
    assert re.match(la_regex, "la $t1, 0($t1)") is not None


def test_move():
    """Test the move instruction."""
    move_regex = Instructions["move"].regex
    assert re.match(move_regex, "move $t1, $t0") is not None
    assert re.match(move_regex, "move $t1, $hi") is None
    assert re.match(move_regex, "move $zero, $t1") is not None
    assert re.match(move_regex, "move $t1, $zero") is not None


def test_beq():
    """Test the beq instruction."""
    beq_regex = Instructions["beq"].regex
    assert re.match(beq_regex, "beq $zero, $t1") is None
    assert re.match(beq_regex, "beq $zero, $t1, label") is not None
    assert re.match(beq_regex, "beq $t1") is None


def test_beqz():
    """Test the beqz instruction."""
    beqz_regex = Instructions["beqz"].regex
    assert re.match(beqz_regex, "beqz $zero, $t1, label") is None
    assert re.match(beqz_regex, "beqz $zero, $t1") is None
    assert re.match(beqz_regex, "beqz $zero, label") is not None


def test_bne():
    """Test the bne instruction."""
    bne_regex = Instructions["bne"].regex
    assert re.match(bne_regex, "bne $zero, $t1, label") is not None
    assert re.match(bne_regex, "bne $zero, label") is None
    assert re.match(bne_regex, "bne $zero") is None
    assert re.match(bne_regex, "bne $zero, $t1, $s1") is None


def test_bge():
    """Test the bge instruction."""
    bge_regex = Instructions["bge"].regex
    assert re.match(bge_regex, "bge $zero, $t1, label") is not None
    assert re.match(bge_regex, "bge $zero, label") is None
    assert re.match(bge_regex, "bge $zero") is None
    assert re.match(bge_regex, "bge $zero, $t1, $s1") is None


def test_bgez():
    """Test the bgez instruction."""
    bgez_regex = Instructions["bgez"].regex
    assert re.match(bgez_regex, "bgez $zero, $t1, label") is None
    assert re.match(bgez_regex, "bgez $zero, label") is not None
    assert re.match(bgez_regex, "bgez $zero") is None
    assert re.match(bgez_regex, "bgez $zero, $t1, $s1") is None


def test_bgt():
    """Test the bgt instruction."""
    bgt_regex = Instructions["bgt"].regex
    assert re.match(bgt_regex, "bgt $zero, $t1, label") is not None
    assert re.match(bgt_regex, "bgt $zero, label") is None
    assert re.match(bgt_regex, "bgt $zero") is None
    assert re.match(bgt_regex, "bgt $zero, $t1, $s1") is None


def test_bgtz():
    """Test the bgtz instruction."""
    bgtz_regex = Instructions["bgtz"].regex
    assert re.match(bgtz_regex, "bgtz $zero, $t1, label") is None
    assert re.match(bgtz_regex, "bgtz $zero, label") is not None
    assert re.match(bgtz_regex, "bgtz $zero") is None
    assert re.match(bgtz_regex, "bgtz $zero, $t1, $s1") is None


def test_ble():
    """Test the ble instruction."""
    ble_regex = Instructions["ble"].regex
    assert re.match(ble_regex, "ble $zero, $t1, label") is not None
    assert re.match(ble_regex, "ble $zero, label") is None
    assert re.match(ble_regex, "ble $zero") is None
    assert re.match(ble_regex, "ble $zero, $t1, $s1") is None


def test_blez():
    """Test the blez instruction."""
    blez_regex = Instructions["blez"].regex
    assert re.match(blez_regex, "blez $zero, $t1, label") is None
    assert re.match(blez_regex, "blez $zero, label") is not None
    assert re.match(blez_regex, "blez $zero") is None
    assert re.match(blez_regex, "blez $zero, $t1, $s1") is None


def test_blt():
    """Test the blt instruction."""
    blt_regex = Instructions["blt"].regex
    assert re.match(blt_regex, "blt $zero, $t1, label") is not None
    assert re.match(blt_regex, "blt $zero, label") is None
    assert re.match(blt_regex, "blt $zero") is None
    assert re.match(blt_regex, "blt $zero, $t1, $s1") is None


def test_bltz():
    """Test the bgtz instruction."""
    bltz_regex = Instructions["bltz"].regex
    assert re.match(bltz_regex, "bltz $zero, $t1, label") is None
    assert re.match(bltz_regex, "bltz $zero, label") is not None
    assert re.match(bltz_regex, "bltz $zero") is None
    assert re.match(bltz_regex, "bltz $zero, $t1, $s1") is None


def test_div():
    """Test the div instruction."""
    div_regex = Instructions["div"].regex
    assert re.match(div_regex, "div $t1, $t2") is not None
    assert re.match(div_regex, "div $t1, 32") is None


def test_mul():
    """Test the mul instruction."""
    mul_regex = Instructions["mul"].regex
    assert re.match(mul_regex, "mul $t1, $t2, $t3") is not None
    assert re.match(mul_regex, "mul $t1, $t2") is None
    assert re.match(mul_regex, "mul $t1, $t2, 33") is None
    assert re.match(mul_regex, "mul $t1, 33, $t3") is None
    assert re.match(mul_regex, "mul 33, $t2, $t3") is None
    assert re.match(mul_regex, "mul $t1") is None


def test_mult():
    """Test the mult instruction."""
    mult_regex = Instructions["mult"].regex
    assert re.match(mult_regex, "mult $t1, $t2") is not None
    assert re.match(mult_regex, "mult $t1, 33") is None
    assert re.match(mult_regex, "mult $t1, 33, $t3") is None
    assert re.match(mult_regex, "mult 33, $t2, $t3") is None
    assert re.match(mult_regex, "mult $t1") is None


def test_mfhi():
    """Test the mfhi instruction."""
    mfhi_regex = Instructions["mfhi"].regex
    assert re.match(mfhi_regex, "mfhi $t1") is not None
    assert re.match(mfhi_regex, "mfhi 33") is None


def test_mflo():
    """Test the mflo instruction."""
    mflo_regex = Instructions["mflo"].regex
    assert re.match(mflo_regex, "mflo $t1") is not None
    assert re.match(mflo_regex, "mflo 33") is None


def test_and():
    """Test the and instruction."""
    and_regex = Instructions["and"].regex
    assert re.match(and_regex, "and $t1, $t2, $t1") is not None
    assert re.match(and_regex, "and $t1, $t2") is None
    assert re.match(and_regex, "and $t1, $t2, 33") is None


def test_andi():
    """Test the andi instruction."""
    andi_regex = Instructions["andi"].regex
    assert re.match(andi_regex, "andi $t1, $t2, $t1") is None
    assert re.match(andi_regex, "andi $t1, $t2") is None
    assert re.match(andi_regex, "andi $t1, $t2, 33") is not None


def test_or():
    """Test the or instruction."""
    or_regex = Instructions["or"].regex
    assert re.match(or_regex, "or $t1, $t2, $t1") is not None
    assert re.match(or_regex, "or $t1, $t2") is None
    assert re.match(or_regex, "or $t1, $t2, 33") is None


def test_nor():
    """Test the nor instruction."""
    nor_regex = Instructions["nor"].regex
    assert re.match(nor_regex, "nor $t1, $t2, $t1") is not None
    assert re.match(nor_regex, "nor $t1, $t2") is None
    assert re.match(nor_regex, "nor $t1, $t2, 33") is None


def test_ori():
    """Test the ori instruction."""
    ori_regex = Instructions["ori"].regex
    assert re.match(ori_regex, "ori $t1, $t2, $t1") is None
    assert re.match(ori_regex, "ori $t1, $t2") is None
    assert re.match(ori_regex, "ori $t1, $t2, 33") is not None


def test_xor():
    """Test the xor instruction."""
    xor_regex = Instructions["xor"].regex
    assert re.match(xor_regex, "xor $t1, $t2, $t1") is not None
    assert re.match(xor_regex, "xor $t1, $t2") is None
    assert re.match(xor_regex, "xor $t1, $t2, 33") is None


def test_xori():
    """Test the xori instruction."""
    xori_regex = Instructions["xori"].regex
    assert re.match(xori_regex, "xori $t1, $t2, $t1") is None
    assert re.match(xori_regex, "xori $t1, $t2") is None
    assert re.match(xori_regex, "xori $t1, $t2, 33") is not None


def test_li():
    """Test the li instruction."""
    li_regex = Instructions["li"].regex
    assert re.match(li_regex, "li $t1, 1") is not None
    assert re.match(li_regex, "li $t1, 99999") is not None
    assert re.match(li_regex, "li $t1, $zero") is None
    assert re.match(li_regex, 'li $t1, "Hello"') is None
    assert re.match(li_regex, "li $t1") is None
    assert re.match(li_regex, "li 99, $t1") is None


def test_lb():
    """Test the lb instruction."""
    lb_regex = Instructions["lb"].regex
    assert re.match(lb_regex, "lb $t1, -100($t2)") is not None
    assert re.match(lb_regex, "lb $t1, 1") is None
    assert re.match(lb_regex, "lb $t1, $zero") is None
    assert re.match(lb_regex, 'lb $t1, "Hello"') is None
    assert re.match(lb_regex, "lb $t1") is None
    assert re.match(lb_regex, "lb 99, $t1") is None


def test_sb():
    """Test the sb instruction."""
    sb_regex = Instructions["sb"].regex
    assert re.match(sb_regex, "sb $t1, -100($t2)") is not None
    assert re.match(sb_regex, "sb $t1, 1") is None
    assert re.match(sb_regex, "sb $t1, $zero") is None
    assert re.match(sb_regex, 'sb $t1, "Hello"') is None
    assert re.match(sb_regex, "sb $t1") is None
    assert re.match(sb_regex, "sb 99, $t1") is None


def test_jal():
    """Test the jal instruction."""
    jal_regex = Instructions["jal"].regex
    assert re.match(jal_regex, "jal label") is not None
    assert re.match(jal_regex, "jal $t1") is None


def test_jalr():
    """Test the jalr instruction."""
    jalr_regex = Instructions["jalr"].regex
    assert re.match(jalr_regex, "jalr label") is None
    assert re.match(jalr_regex, "jalr $t1, $t2") is not None


def test_j():
    """Test the j instruction."""
    j_regex = Instructions["j"].regex
    assert re.match(j_regex, "j label") is not None
    assert re.match(j_regex, "j $t1") is None
    assert re.match(j_regex, "j 1") is not None
    assert re.match(j_regex, "j label1, label2") is not None


def test_b():
    """Test the b instruction."""
    b_regex = Instructions["b"].regex
    assert re.match(b_regex, "b label") is not None
    assert re.match(b_regex, "b $t1") is None
    assert re.match(b_regex, "b 1") is not None
    assert re.match(b_regex, "b label1, label2") is not None


def test_syscall():
    """Test the syscall instruction."""
    syscall_regex = Instructions["syscall"].regex
    assert re.match(syscall_regex, "syscall") is not None
