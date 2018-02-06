import copy

def bounds_check_elimination(ast, MAX):
    final = {}
    for name in ast:
        final[name] = []
        stack_min = 0
        for op_type, op, _ in ast[name]:
            final[name].append((op_type, op, stack_min))
            if op_type == 'INT':
                stack_min += 1
            elif op_type == 'ADD':
                if isinstance(op, str):
                    stack_min = max(1, stack_min - 1)
                else:
                    stack_min = max(1, stack_min)
            elif op_type == 'SUB':
                if isinstance(op, str):
                    stack_min = max(1, stack_min - 1)
                else:
                    stack_min = max(1, stack_min)
            elif op_type == 'MUL':
                if isinstance(op, str):
                    stack_min = max(1, stack_min - 1)
                else:
                    stack_min = max(1, stack_min)
            elif op_type == 'DIV':
                if isinstance(op, str):
                    stack_min = max(1, stack_min - 1)
                else:
                    stack_min = max(1, stack_min)
            elif op_type == 'STORE':
                if isinstance(op, str):
                    stack_min = max(0, stack_min - 2)
                elif isinstance(op, int):
                    stack_min = max(0, stack_min - 1)
            elif op_type == 'LOAD':
                if isinstance(op, str):
                    stack_min = max(1, stack_min)
                else:
                    stack_min += 1
            elif op_type == 'DUP':
                stack_min += 1
            elif op_type == 'EQ':
                if isinstance(op, str):
                    stack_min = max(1, stack_min - 1)
                else:
                    stack_min = max(1, stack_min)
            elif op_type == 'NT':
                if isinstance(op, str):
                    stack_min = max(1, stack_min)
                else:
                    stack_min += 1
            elif op_type == 'GREATER':
                if isinstance(op, str):
                    stack_min = max(1, stack_min - 1)
                else:
                    stack_min = max(1, stack_min)
            elif op_type == 'LESS':
                if isinstance(op, str):
                    stack_min = max(1, stack_min - 1)
                else:
                    stack_min = max(1, stack_min)
            elif op_type == 'MOD':
                if isinstance(op, str):
                    stack_min = max(1, stack_min - 1)
                else:
                    stack_min = max(1, stack_min)
            elif op_type == 'INPUT':
                stack_min += 1
            elif op_type == 'OUTPUT':
                if isinstance(op, str):
                    stack_min = max(0, stack_min - 1)
            elif op_type == 'OUTPUT_NUM':
                stack_min = max(0, stack_min - 1)
            else:
                print('Unknown op_type:', op_type, op)
    return final

def partial_evaluation(ast, MAX):
    final = {}
    for name in ast:
        final[name] = []
        stack = []
        mem = {}
        for op_type, op, _ in ast[name]:
            if isinstance(op, tuple):
                stack.extend(op)
            elif isinstance(op, int):
                stack.append(op)
            
            if op_type == 'INT':
                pass
            elif op_type == 'ADD':
                if len(stack) >= 2:
                    now = stack[-2] + stack[-1]
                    del stack[-2:]
                    stack.append(now % MAX)
                elif stack:
                    final[name].append(('ADD', stack.pop(), 0))
                else:
                    final[name].append(('ADD', op, 0))
            elif op_type == 'SUB':
                if len(stack) >= 2:
                    now = stack[-2] - stack[-1]
                    del stack[-2:]
                    stack.append(now % MAX)
                elif stack:
                    final[name].append(('SUB', stack.pop(), 0))
                else:
                    final[name].append(('SUB', op, 0))
            elif op_type == 'MUL':
                if len(stack) >= 2:
                    now = stack[-2] * stack[-1]
                    del stack[-2:]
                    stack.append(now % MAX)
                elif stack:
                    final[name].append(('MUL', stack.pop(), 0))
                else:
                    final[name].append(('MUL', op, 0))
            elif op_type == 'DIV':
                if len(stack) >= 2:
                    try:
                        now = stack[-2] / stack[-1]
                    except ZeroDivisionError:
                        now = 17
                    del stack[-2:]
                    stack.append(now % MAX)
                elif stack:
                    final[name].append(('DIV', stack.pop(), 0))
                else:
                    final[name].append(('DIV', op, 0))
            elif op_type == 'STORE':
                if len(stack) >= 2:
                    mem[stack[-1]] = stack[-2]
                    del stack[-2:]
                elif stack:
                    if stack[-1] in mem:
                        del mem[stack[-1]]
                    final[name].append(('STORE', stack.pop(), 0))
                else:
                    final[name].append(('STORE', op, 0))
            elif op_type == 'LOAD':
                if stack:
                    if stack[-1] in mem:
                        stack.append(mem[stack.pop()])
                    else:
                        for stack_min, i in enumerate(stack[:-1]):
                            final[name].append(('INT', i, stack_min))
                        final[name].append(('LOAD', stack[-1], len(stack)))
                        stack.clear()
                else:
                    final[name].append(('LOAD', op, 0))
            elif op_type == 'DUP':
                if stack:
                    stack.append(stack[-1])
                else:
                    final[name].append(('DUP', op, 0))
            elif op_type == 'EQ':
                if len(stack) >= 2:
                    now = int(stack[-2] == stack[-1])
                    del stack[-2:]
                    stack.append(now)
                elif stack:
                    final[name].append(('EQ', stack.pop(), 0))
                else:
                    final[name].append(('EQ', op, 0))
            elif op_type == 'NT':
                if stack:
                    stack.append(int(not stack.pop(-1)))
                else:
                    final[name].append(('NT', op, 0))
            elif op_type == 'GREATER':
                if len(stack) >= 2:
                    now = int(stack[-2] > stack[-1])
                    del stack[-2:]
                    stack.append(now)
                elif stack:
                    final[name].append(('GREATER', stack.pop(), 0))
                else:
                    final[name].append(('GREATER', op, 0))
            elif op_type == 'LESS':
                if len(stack) >= 2:
                    now = int(stack[-2] < stack[-1])
                    del stack[-2:]
                    stack.append(now)
                elif stack:
                    final[name].append(('LESS', stack.pop(), 0))
                else:
                    final[name].append(('LESS', op, 0))
            elif op_type == 'MOD':
                if len(stack) >= 2:
                    now = stack[-2] % stack[-1]
                    del stack[-2:]
                    stack.append(now % MAX)
                elif stack:
                    final[name].append(('MOD', stack.pop(), 0))
                else:
                    final[name].append(('MOD', op, 0))
            elif op_type == 'INPUT':
                for stack_min, i in enumerate(stack):
                    final[name].append(('INT', i, stack_min))
                final[name].append(('INPUT', op, len(stack)))
                stack.clear()
            elif op_type == 'OUTPUT':
                if stack:
                    final[name].append(('OUTPUT', [stack.pop()], 0))
                else:
                    final[name].append(('OUTPUT', op, 0))
            elif op_type == 'OUTPUT_NUM':
                if stack:
                    final[name].append(('OUTPUT',
                                        list(map(ord, str(stack.pop()))), 0))
                else:
                    final[name].append(('OUTPUT_NUM', op, 0))
            else:
                for stack_min, i in enumerate(stack):
                    final[name].append(('INT', i, stack_min))
                for key in mem:
                    final[name].append(('STORE', (mem[key], key), 0))
                mem.clear()
                final[name].append((op_type, op, len(stack)))
                stack.clear()
                print('Unknown op_type:', op_type, op)
        for stack_min, i in enumerate(stack):
            final[name].append(('INT', i, stack_min))
        for key in sorted(mem, reverse=True):
            final[name].append(('STORE', (mem[key], key), 0))
        mem.clear()
    return final
        

def peephole(ast, MAX):
    changed = True
    while changed:
        changed = False 
        for name in ast:
            block = ast[name]
            for i, x in enumerate(block):
                try:
                    if x[0] == 'OUTPUT' and block[i + 1][0] == 'OUTPUT':
                        if isinstance(block[i][1], list):
                            if isinstance(block[i + 1][1], list):
                                block[i:i + 2] = [('OUTPUT',
                                                   x[1] + block[i + 1][1],
                                                   block[i][2])]
                                changed = True
                except IndexError:
                    pass
                if changed:
                    ast[name] = block
                    break
    return ast

def loop_unrolling(ast, MAX):
    for name in ast:
        if ast[name][-1][0] == 'STORE':
            if isinstance(ast[name][-1][1], tuple):
                #print(ast[name][-1])
                if ast[name][-1][1][1] == 0:
                    num = ast[name][-1][1][0]
                    if num in ast:
                        ast[name].extend(ast[num])
    return ast

def dead_code_elimination(ast, MAX):
    if ast[2149][-1][0] == 'STORE':
        if isinstance(ast[2149][-1][1], tuple):
            if ast[2149][-1][1][1] == 0:
                if ast[2149][-1][1][0] not in ast:
                    return {2149: ast[2149]}
    return ast


def optimize(ast, MAX, OPTIMIZE):
    for i in range(OPTIMIZE * 10):
        old = copy.copy(ast)
        ast = partial_evaluation(ast, MAX)
        ast = dead_code_elimination(ast, MAX)
        ast = peephole(ast, MAX)
        ast = loop_unrolling(ast, MAX)
        if ast == old:
            break
    ast = bounds_check_elimination(ast, MAX)
    return ast
