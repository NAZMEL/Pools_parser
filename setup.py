from cx_Freeze import setup, Executable

base = None

includes = ['grab.transport.curl']
excludes = []
include_files = ['suprnova.py', 'Resource']
executables = [Executable("parse_pool.py", base=base)]


packages = ["idna"]
options = {
    'build_exe': {
        'packages':packages,
        'include_files': include_files,
        'includes': includes,
        'excludes': excludes
    },
}

setup(
    name = "parse_pool",
    options = options,
    version = "1.1.0",
    description = '<any description>',
    executables = executables
)