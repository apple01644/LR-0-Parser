import time
from pathlib import Path
from typing import List

from lr_0_parser.compiler import Compiler
from lr_0_parser.compiler_builder import CompilerBuilder
from lr_0_parser.compiler_env import CompilerEnvironment
from lr_0_parser.defines import CFG, ParseTree
from lr_0_parser.report_maker import ReportMaker


class MainProgram:
    def __init__(self, env: CompilerEnvironment):
        self.env: CompilerEnvironment = env
        # Output Paths
        self.path_report_item_set: Path = Path('report/report_item_set.txt')
        self.path_report_cfg: Path = Path('report/report_cfg.txt')
        self.path_report_transition: Path = Path('report/report_transition.txt')
        self.path_parse_tree: Path = Path('report/report_parse_tree.txt')

    def main_process(self, input_tokens: List[str]):
        report_maker = ReportMaker(env=self.env)
        report_maker.report_of_cfg(output_path=self.path_report_cfg)
        self.validate_cfg()
        compiler_builder = CompilerBuilder(env=env)
        compiler_builder.build_compiler()
        report_maker.report_of_item_sets(output_path=self.path_report_item_set, compiler_builder=compiler_builder)
        report_maker.report_of_transitions(output_path=self.path_report_transition)
        output_parse_tree: ParseTree = Compiler(env=env).main_process(iter(input_tokens))
        report_maker.report_of_parse_tree(output_path=self.path_parse_tree, parse_tree=output_parse_tree)

    def validate_cfg(self):
        for k, cfg in enumerate(self.env.cfg_list):
            symbols = [cfg.lhs] + cfg.rhs
            for sym in symbols:
                if sym in self.env.terminals:
                    continue
                if sym in self.env.non_terminals:
                    continue
                if sym == self.env.eof_symbol:
                    continue
                raise ValueError('{} is not appropriate symbol'.format(sym))
            cfg.id = k


if __name__ == '__main__':
    try:
        env = CompilerEnvironment()

        env.terminals = ['0', '1', '+', '*', '(', ')']
        env.non_terminals = ['E', 'M', 'B']
        env.cfg_list = [
            CFG('E', ['M']),
            CFG('E', ['E', '+', 'M']),
            CFG('M', ['B']),
            CFG('M', ['M', '*', 'B']),
            CFG('B', ['(', 'E', ')']),
            CFG('B', ['0']),
            CFG('B', ['1']),
        ]
        MainProgram(env=env).main_process(
            list('1*(1+0)')
        )
    finally:
        time.sleep(0.1)
