from io import StringIO
from pathlib import Path

from lr_0_parser.action import Action
from lr_0_parser.compiler_builder import CompilerBuilder
from lr_0_parser.compiler_env import CompilerEnvironment
from lr_0_parser.defines import ParseTree


class ReportMaker:
    def __init__(self, env: CompilerEnvironment):
        self.env: CompilerEnvironment = env

    def report_of_cfg(self, output_path: Path) -> str:
        ss = StringIO()
        for cfg in self.env.cfg_list:
            print(cfg.lhs, '→', ' '.join(cfg.rhs), file=ss)
        content = ss.getvalue()
        output_path.write_text(content, encoding='utf-8')
        return content

    def report_of_item_sets(self, output_path: Path, compiler_builder: CompilerBuilder) -> str:
        ss = StringIO()
        for item_set in compiler_builder.item_sets:
            print(item_set, file=ss)
        content = ss.getvalue()
        output_path.write_text(content, encoding='utf-8')
        return content

    def report_of_transitions(self, output_path: Path) -> str:
        ss = StringIO()
        ui_col_size = 3
        ui_col_head_size = 7
        ui_col_fmt = '%{}s'.format(ui_col_size)
        ui_col_head_fmt = '%{}s'.format(ui_col_head_size)
        cols = self.env.terminals + [self.env.eof_symbol] + self.env.non_terminals
        sep = ' | '
        # Write Row Header
        row_head_text = ui_col_head_fmt % 'ItemSet' + sep
        for col in cols:
            row_head_text += ui_col_fmt % col + sep
        print(row_head_text, file=ss)
        print('-' * len(row_head_text), file=ss)
        # Write Content
        for row_idx in range(self.env.item_set_size):
            try:
                action_row = self.env.action_table.rows[row_idx]
            except KeyError:
                action_row = None
            try:
                goto_row = self.env.goto_table.rows[row_idx]
            except KeyError:
                goto_row = None
            # Col Header
            row_text = ''
            row_text += ui_col_head_fmt % row_idx + sep
            # Terminals and EOF
            for sym in self.env.terminals + [self.env.eof_symbol]:
                data = ''
                if action_row and sym in action_row:
                    act = action_row[sym]
                    if act.tp_cd == Action.SHIFT:
                        data = 's%d' % act.shift_item_set_id
                    elif act.tp_cd == Action.REDUCE:
                        data = 'r%d' % act.reduce_cfg_id
                    elif act.tp_cd == Action.ACCEPT:
                        data = 'acc'
                row_text += ui_col_fmt % data + sep
            # Non-Terminals
            for sym in self.env.non_terminals:
                data = ''
                if goto_row and sym in goto_row:
                    data = '%d' % goto_row[sym]
                row_text += ui_col_fmt % data + sep
            print(row_text, file=ss)
        content = ss.getvalue()
        output_path.write_text(content, encoding='utf-8')
        return content

    def report_of_parse_tree(self, output_path: Path, parse_tree: ParseTree) -> str:
        ss = StringIO()
        print(parse_tree, file=ss)
        content = ss.getvalue()
        output_path.write_text(content, encoding='utf-8')
        return content
