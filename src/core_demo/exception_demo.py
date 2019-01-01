# runtime error就是exception
# except后面无Error时，捕获所有异常，但不是推荐的做法，因为异常原因未知


class Error(Exception):
    pass


class InputTooSmallError(Exception):
    pass


class InputTooBigError(Exception):
    pass


alphabet = 'm'
while True:
    apb = input('Enter a alphabet: ')
    try:
        if apb < alphabet:
            raise InputTooSmallError
        elif apb > alphabet:
            raise InputTooBigError
    # except后面可以有多种Error
    except InputTooSmallError:
        print('The entered alphabet is too small, try again!')
        print('')
    except InputTooBigError:
        print('the entered alphabet is too big, try again!')
        print('')
    # else结构，无异常时执行
    else:
        break
    finally:
        print('finally')
print('congratulation!')

# 内置异常
# ArithmeticError	For errors in numeric calculation.
# AssertionError	If the assert statement fails.
# AttributeError	When an attribute assignment or the reference fails.
# EOFError	If there is no input or the file pointer is at EOF.
# Exception	It is the base class for all exceptions.
# EnvironmentError	For errors that occur outside the Python environment.
# FloatingPointError	When floating point operation fails.
# GeneratorExit	If a generator’s <close()> method gets called.
# ImportError	When the imported module is not available.
# IOError	If an input/output operation fails.
# IndexError	When the index of a sequence is out of range.
# KeyError	If the specified key is not available in the dictionary.
# KeyboardInterrupt	When the user hits an interrupt key (Ctrl+c or delete).
# MemoryError	If an operation runs out of memory.
# NameError	When a variable is not available in local or global scope.
# NotImplementedError	If an abstract method isn’t available.
# OSError	When a system operation fails.
# OverflowError	If the result of an arithmetic operation exceeds the range.
# ReferenceError	When a weak reference proxy accesses a garbage collected reference.
# RuntimeError	If the generated error doesn’t fall under any category.
# StandardError	It is a base class for all built-in exceptions except <StopIteration> and <SystemExit>.
# StopIteration	The <next()> function has no further item to be returned.
# SyntaxError	For errors in Python syntax.
# IndentationError	When indentation is not proper.
# TabError	For inconsistent tabs and spaces.
# SystemError	When interpreter detects an internal error.
# SystemExit	The <sys.exit()> function raises it.
# TypeError	When a function is using an object of the incorrect type.
# UnboundLocalError	If the code using an unassigned reference gets executed.
# UnicodeError	For a Unicode encoding or decoding error.
# ValueError	When a function receives invalid values.
# ZeroDivisionError	If the second operand of division or modulo operation is zero.
