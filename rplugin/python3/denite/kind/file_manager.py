# ============================================================================
# FILE: file_manager.py
# AUTHOR: 年糕小豆汤 <ooiss@qq.com>
# License: MIT license
# ============================================================================

import os
import shutil
from pathlib import Path
from denite import util
from .base import Base as BaseKind


class Kind(BaseKind):
    def __init__(self, vim):
        super().__init__(vim)

        self.persist_actions += ['add', 'delete', 'move', 'rename', 'copy']
        self.redraw_actions += ['add', 'delete', 'move', 'rename', 'copy']
        self.name = 'file_manager'

    def action_add(self, context):
        target = context['targets'][0]
        path = target['action__path']
        content = util.input(self.vim, context, 'Add (dir end with /): ')
        if not len(content):
            return
        if content.endswith('/'):
            os.makedirs(os.path.join(path, content))
        else:
            Path(os.path.join(path, content)).touch()

    def action_delete(self, context):
        target = context['targets'][0]
        path = target['action__path']
        content = util.input(self.vim, context, 'Delete ({}): yes/no ? '.format(path))
        if content == 'yes':
            if os.path.isdir(path):
                os.removedirs(path)
            else:
                os.remove(path)
        elif content == 'yes!':
            if os.path.isdir(path):
                shutil.rmtree(path)
            else:
                os.remove(path)


    def action_move(self, context):
        target = context['targets'][0]
        path = target['action__path']
        content = util.input(self.vim, context, 'Move to: ', path)
        if not len(content):
            return
        shutil.move(path, content)

    def action_rename(self, context):
        target = context['targets'][0]
        path = target['action__path']
        content = util.input(self.vim, context, 'Rename to: ', path)
        if not len(content):
            return
        os.rename(path, content)

    def action_copy(self, context):
        target = context['targets'][0]
        path = target['action__path']
        content = util.input(self.vim, context, 'Rename to: ', path)
        if not len(content):
            return
        if os.path.isdir(path):
            shutil.copytree(path, content)
        else:
            shutil.copyfile(path, content)
