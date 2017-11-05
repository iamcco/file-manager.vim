# ============================================================================
# FILE: file_manager_dir.py
# AUTHOR: 年糕小豆汤 <ooiss@qq.com>
# License: MIT license
# ============================================================================

from .directory import Kind  as DirectoryKind
from .file_manager import Kind  as FileManagerKind


class Kind(FileManagerKind, DirectoryKind):
    def __init__(self, vim):
        super().__init__(vim)

        self.default_action = 'narrow'
        self.name = 'file_manager_dir'

    def action_narrow(self, context):
        target = context['targets'][0]
        context['input'] = target['abbr']
