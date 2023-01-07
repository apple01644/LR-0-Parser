import itertools
from typing import List, Optional, Iterator

from lr_0_parser.action import Action
from lr_0_parser.compiler_env import CompilerEnvironment
from lr_0_parser.defines import ParseTree


class Compiler:
    def __init__(self, env: CompilerEnvironment):
        self.env: CompilerEnvironment = env

    def main_process(self, input_tokens: Iterator[str]) -> ParseTree:
        input_tokens = itertools.chain(input_tokens, [self.env.eof_symbol])
        state_stack: List[int] = [0]
        output_stack: List[ParseTree] = list()
        lookahead: Optional[str] = None
        try:
            for x in range(1000):
                state_id: int = state_stack[-1]
                if lookahead is None and input_tokens:
                    try:
                        lookahead = next(input_tokens)
                    except StopIteration:
                        input_tokens = None
                # Read Goto Table
                if output_stack and state_id in self.env.goto_table.rows:
                    goto_row = self.env.goto_table.rows[state_id]
                    top = output_stack[-1].lhs
                    if top in goto_row:
                        state_stack.append(goto_row[top])
                        continue

                # Read Action Table
                if lookahead is not None:
                    action_row = self.env.action_table.rows[state_id]
                    try:
                        act = action_row[lookahead]
                    except KeyError as ke:
                        raise ke
                    if act.tp_cd == Action.SHIFT:
                        output_stack.append(ParseTree(lookahead))
                        state_stack.append(act.shift_item_set_id)
                        print('> SHIFT', lookahead, ':', state_id, 'to ', act.shift_item_set_id)
                        lookahead = None
                        continue
                    elif act.tp_cd == Action.REDUCE:
                        cfg = self.env.cfg_list[act.reduce_cfg_id]
                        org_state_id = state_id
                        print('> REDUCE with', cfg)
                        new_parser_tree = ParseTree(cfg.lhs)
                        for expect_sym in reversed(cfg.rhs):
                            output = output_stack.pop(-1)
                            assert expect_sym == output.lhs
                            new_parser_tree.rhs.insert(0, output)
                            state_stack.pop(-1)
                        new_state_id = state_stack[-1]
                        print('    >', org_state_id, 'to', new_state_id)
                        output_stack.append(new_parser_tree)
                        continue
                    elif act.tp_cd == Action.ACCEPT:
                        print('> ACCEPT')
                        print(output_stack[0])
                        break
                raise EOFError()
        except Exception as e:
            print('ERROR: meets', lookahead)
            print('STATE =', state_stack[-1], 'of', state_stack)
            for k, output in enumerate(output_stack):
                print('OUTPUT[%2d]' % k, '-' * 20)
                print(output)
            raise e
        return output_stack[-1]
