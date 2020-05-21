from app import Optionsjson

op = Optionsjson

try:
    op.writejason(op.setdata('estudantes'), 'estudantes')
    exit(0)
except FileNotFoundError:
    exit(1)
