# ============================================================================
# FILE: file_manager.py
# AUTHOR: 年糕小豆汤 <ooiss@qq.com>
# License: MIT license
# ============================================================================

import glob
import os
from denite.util import abspath
from .file_rec import Source as Rec


class Source(Rec):

    def __init__(self, vim):
        super().__init__(vim)

        self.name = 'file_manager'

    def on_init(self, context):
        context['is_interactive'] = True
        if not context['is_windows'] and not self.vars['command']:
            self.vars['command'] = [
                'find', '-L', ':directory',
                '-path', '*/.git/*', '-prune', '-o',
                '-type', 'l', '-print', '-o', '-type', 'd', '-print']

        super().on_init(context)

    def gather_candidates(self, context):
        candidates = []
        if context['input'].endswith('/'):
            path = (context['args'][1] if len(context['args']) > 1
                    else context['path'])
            filename = (context['input']
                        if os.path.isabs(context['input'])
                        else os.path.join(path, context['input']))
            for f in glob.glob(os.path.dirname(filename) + '/*'):
                relF = os.path.relpath(f, path)
                candidates.append({
                    'word': relF,
                    'abbr': relF + ('/' if os.path.isdir(f) else ''),
                    'kind': ('file_manager_dir' if os.path.isdir(f) else 'file_manager_file'),
                    'action__path': abspath(self.vim, f),
                    })
        else:
            candidates = [x for x in super().gather_candidates(context)
                    if x['action__path'] != context['__directory']]
            for candidate in candidates:
                candidate['abbr'] = candidate['word'] + '/'
                candidate['kind'] = 'file_manager_dir' if os.path.isdir(candidate['action__path']) else 'file_manager_file'
        return candidates
