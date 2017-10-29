# ============================================================================
# FILE: file_manager_file.py
# AUTHOR: 年糕小豆汤 <ooiss@qq.com>
# License: MIT license
# ============================================================================

from .file import Kind  as FileKind
from .file_manager import Kind  as FileManagerKind


class Kind(FileManagerKind, FileKind):
    def __init__(self, vim):
        super().__init__(vim)

        self.default_action = 'open'
        self.name = 'file_manager_file'
