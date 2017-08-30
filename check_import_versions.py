import sys
import types

import pip


# ---------------- Version information check -----------------------------------------

def imports():
    exclude_list = ['builtins', '__builtin__', 'types', 'pip', 'sys', 'py']
    for name, val in globals().items():
        if isinstance(val, types.ModuleType):
            if val.__name__ in exclude_list:
                pass
            else:
                yield val.__name__.split('.')[0]


def imports_list():
    list_of_imports = list(imports())
    imports_list = ', '.join(list_of_imports)
    return imports_list


def python_version_str():
    return 'Python: ' + str(sys.version_info[0]) + '.' + str(sys.version_info[1])


def imports_version_info():
    import_list_with_versions = \
        [
            pkg.key + ': ' + pkg.version
            for pkg in pip.get_installed_distributions()
            if pkg.key in imports_list()
        ]
    import_list_with_versions.insert(0, python_version_str())
    return import_list_with_versions


print imports_version_info()

# ------------ End version information check -----------------------------------------
