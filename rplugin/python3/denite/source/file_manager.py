# ============================================================================
# FILE: file_manager.py
# AUTHOR: 年糕小豆汤 <ooiss@qq.com>
# License: MIT license
# ============================================================================

import glob
import os
import shutil
from pathlib import Path
from denite import util
from denite.kind.base import Base as BaseKind
from denite.kind.file import Kind  as FileKind
from denite.kind.directory import Kind  as DirectoryKind
from denite.source.file_rec import Source as Rec

class FileManagerBaseKind(BaseKind):
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

class DirectoryManagerKind(FileManagerBaseKind, DirectoryKind):
    def __init__(self, vim):
        super().__init__(vim)

        self.default_action = 'narrow'
        self.name = 'file_manager_dir'

    def action_narrow(self, context):
        target = context['targets'][0]
        context['input'] = target['abbr']

class FileManagerKind(FileManagerBaseKind, FileKind):
    def __init__(self, vim):
        super().__init__(vim)

        self.default_action = 'open'
        self.name = 'file_manager_files'

class Source(Rec):

    def __init__(self, vim):
        super().__init__(vim)

        self.name = 'file_manager'
        self.fileKind = FileManagerKind(vim)
        self.directoryKind = DirectoryManagerKind(vim)

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
                    'kind': (self.directoryKind if os.path.isdir(f) else self.fileKind),
                    'action__path': util.abspath(self.vim, f),
                    })
        else:
            candidates = [x for x in super().gather_candidates(context)
                    if x['action__path'] != context['__directory']]
            for candidate in candidates:
                candidate['abbr'] = candidate['word'] + '/'
                candidate['kind'] = self.directoryKind if os.path.isdir(candidate['action__path']) else self.fileKind
        return candidates
