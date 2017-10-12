#!/usr/bin/env python
import sympy
import matplotlib.pyplot as pyplot
import time
sympy.var('a b c d w x y z ')
class pl_true:
    def __init__(self, sentence):
        self.model = {x:True,y:False,z:True,a:False,c:False}
        self.expr = sentence
        self.expr=self.make_simple()
        print("Given Sentence:")
        print(self.expr)
        self.expr = sympy.to_cnf(self.expr)
        # print('in CNF:')
        # print(self.expr)
        self.result=self.logic_solver(self.expr)
        print ("Result")
        print self.result

    def make_simple(self):
        # to remove the biconditional and implication operator and
        # replace it appopriate sympy operator
        simple = self.expr;
        s =1
        while (simple.count('<==>'))>0:
            simple = '('+self.expr.replace('<==>','>>',s) +')&(' +self.expr.replace('<==>','<<',s) + ')'
            s+=1
        try:
            simple=simple.replace('=>','>>')
        except:
            simple=self.expr.replace('=>','>>')
        return simple

    def expr_length_cnf(self):
        return len(self.expr.args)

    def logic_solver(self,sentence):
        result =[]
        if len(sentence.args) ==0  or len(sentence.args) ==1 :
            sentence = sentence.subs(self.model);
            return sentence
        if len(sentence.args) ==2:
            sentence = sentence.subs(self.model);
            for x in sentence.atoms():
                if self.model.has_key(x):
                    continue
                sentence=sympy.simplify(sentence)
            return sentence
        for i in range(0,len(sentence.args)):
            result.append(self.logic_solver(sentence.args[i]))
        if type(sentence) == sympy.Or:
            simple_result = False
            for i in result:
                ##### Modfied Secion for part d Start
                if i == sympy.true:
                    return sympy.true
                ##### End
                simple_result = sympy.Or(simple_result,i)
        if type(sentence) == sympy.And:
            simple_result = True
            for i in result:
                ##### Modfied Secion for part d Start
                if i == sympy.false:
                    return sympy.false
                ##### End
                simple_result = sympy.And(simple_result,i)
        # print result
        # print simple_result
        return simple_result

if __name__== "__main__":
    # w and b are the unkown
    expression = ['((~x|w)=>z)&(x&w)','w|a','y&(z|~y)', '(a)|(x&y)|(a&z)&(z)','(a=>y)=>(x=>z)',
    '(a&x)&(x|z)','((y=>(z|a))&(z|~a)&(a=>z))&((w&~w)|(a=>x))&(x)',
    '(((y=>(z|a))&(z|~a)&(a=>z))&((w&~w)|(a=>x))&(x))=>((a=>y)=>(x=>z))','(y=>(z|a))',
    '(a)<==>(y&~a)','(a&z)|(w&x)|(y&(a=>x))','((a&z)|(w&x)&(y|(a=>x)))<==>(~b|x&z)','~(y|(z&a))&((z|x&~y)=>(c|(z&~w)))',
    '(~c|w)|(x&y)|(a&z)&(z=>~c)','(~x|((a&~b)=>z))<==>(a=>(c&b&x))',
    '((a&z)&(w&x)&(y|(a=>x)))=>(~b|x&z)','(~b&x)=>(((a&z)&(w&x)&(y|(a=>x))))',
    '((w&~w)|(a=>x)&x)=>((a=>y)=>(x=>z))=>((a=>y)=>(x=>z))','(((~x|w)=>z)&(x&w))=>((x=>z)&(y=>(z|a)))',
    '((a&z)&(w&x)&(y|(a=>x)))&((a&z)&(w&x)&(y|(a=>x)))', '(~x|((a&~x)=>z))=>((a)|(x&y)|(a&z)&(z))',
    '~(y|(z&a))<==>((z|x&~y)&(c|(z&~w)))','(((z|x&~y)&(c|(z&~w)))&(~x|((a&~x)=>z)))=>(((w&x)&(y|(a=>x))))'];
    # print(len(expression))
    length_cnf = []
    time_taken =[]
    time.sleep(1)
    for exp in expression:
        start = time.time()
        pl_value = pl_true(exp)
        end =time.time()
        print "Total time taken : %f Seconds "%float(end-start)
        length_cnf.append(pl_value.expr_length_cnf())
        time_taken.append((float(end-start)*1000))
        time.sleep(0.2)
    # print length_cnf
    pyplot.plot(length_cnf,time_taken,'ro')
    pyplot.ylabel('Time taken in milliseconds')
    pyplot.xlabel('Length of Sentence (no of terms in CNF)')
    pyplot.title('No of terms in CNF Vs Time taken to compute')
    pyplot.show()
