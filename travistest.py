
from app import Optionsjson
op = Optionsjson
try:
    op.setdata('estudantes')
    exit(0)
except FileNotFoundError:
    exit(1)

