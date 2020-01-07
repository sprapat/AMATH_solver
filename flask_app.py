from flask import Flask, request, render_template
import itertools
import re

def two_operators_next_to_each_other(formula):
  pattern = r"""[+\-\*/][+\-\*/]"""
  return re.search(pattern, formula) is not None

def operators_next_to_equal_sign(formula):
  p1 = r"""[+\-\*/]=="""
  p2 = r"""==[+\-\*/]"""
  return (re.search(p1, formula) is not None) or \
         (re.search(p2, formula) is not None)

def operator_in_front(formula):
  return formula[0] in '+-*/'

def check_formula(formula):
  left, right = formula.split('==')
  return not two_operators_next_to_each_other(left) and \
         not two_operators_next_to_each_other(right) and \
         not operators_next_to_equal_sign(formula) and \
         not operator_in_front(left) and \
         not operator_in_front(right)

def solve(items):
  result_str = []
  result = set()
  a = list(items)
  a.append('==')
  for i in itertools.permutations(a):
    try:
      formula = ''.join(i)
      if eval(formula) and check_formula(formula):
        result.add(formula)
    except SyntaxError:
      pass
  for item in result:
    new_item = item.replace('==',' = ')
    result_str.append(new_item+'\n')
  return result_str

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def hello_world():
    solution = []
    question = ''
    if request.method == 'POST':
    	question = request.form['question'].strip().replace(' ','').replace('=','')
    	try:
    	  solution = solve(question)
    	except:
    	  solution = []
    else:
    	solution = []
    # the code below is executed if the request method
    # was GET or the credentials were invalid
    return render_template('index.html',question=question, solution=solution)