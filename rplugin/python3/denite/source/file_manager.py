# ============================================================================
# FILE: file_manager.py
# AUTHOR: 年糕小豆汤 <ooiss@qq.com>
# License: MIT license
# ============================================================================

import glob
import os
from denite.util import abspath
from .base import Base


class Source(Base):

    def __init__(self, vim):
        super().__init__(vim)

        self.name = 'file_manager'

    def gather_candidates(self, context):
        context['is_interactive'] = True
        candidates = []
        path = (context['args'][1] if len(context['args']) > 1
                else context['path'])
        filename = (context['input']
                    if os.path.isabs(context['input'])
                    else os.path.join(path, context['input']))
        for f in glob.glob(os.path.dirname(filename) + '/*'):
            candidates.append({
                'word': f,
                'abbr': f + ('/' if os.path.isdir(f) else ''),
                'kind': ('file_manager_dir' if os.path.isdir(f) else 'file_manager_file'),
                'action__path': abspath(self.vim, f),
                })
        return candidates
