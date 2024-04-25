"""Document the source code"""

import inspect
import io
import pydoc
import time
import types
import typing

from tkintertools import constants, exceptions, main, tools_3d


def get_object_type(__object: typing.Any, /, *, module: types.ModuleType | None = None) -> typing.Literal["Class", "Function", "Constant"]:
    """get base type of an object"""
    if module is not None:
        if not isinstance(__object, str):
            raise TypeError("When have mudule, the __object must be a string.")
        __object = getattr(module, __object)
    if inspect.isclass(__object):
        return "Class"
    if inspect.isfunction(__object):
        return "Function"
    return "Constant"


def get_module_menbers(__module: types.ModuleType, /) -> tuple[type | types.FunctionType]:
    """get all menbers in a module"""
    module_path = inspect.getsourcefile(__module)
    menbers = tuple(getattr(__module, menber) for menber in dir(__module))
    menbers = filter(lambda menber: get_object_type(
        menber) != "Constant", menbers)
    menbers = filter(lambda menber: inspect.getsourcefile(
        menber) == module_path, menbers)
    return tuple(menbers)


def get_module_data(__module: types.ModuleType) -> tuple[str]:
    """get all data defined in a module"""
    import_modules = [attr for attr in dir(__module) if isinstance(
        getattr(__module, attr), types.ModuleType)]
    data = [attr for attr in dir(__module) if pydoc.isdata(attr)]
    data = filter(lambda d: d not in import_modules, data)
    for module in import_modules:
        module_data = [attr for attr in dir(
            getattr(__module, module)) if pydoc.isdata(attr)]
        data = filter(lambda d: d not in module_data, data)
    data = filter(lambda c: getattr(__module, c)
                  not in get_module_menbers(__module), data)
    return tuple(data)


def get_class_methods(__class: type, /) -> tuple[types.MethodType, ...]:
    """get all method of a class without inheriate from its super class"""
    super_classes = __class.__bases__
    super_classes_methods = [pydoc.allmethods(cls) for cls in super_classes]
    all_methods = pydoc.allmethods(__class)
    for methods in super_classes_methods:
        all_methods = tuple(
            filter(lambda method: method not in methods, all_methods))
    return tuple(getattr(__class, method) for method in all_methods)


def get_code_block(obj: type, *, language: str = "python") -> list[str]:
    """render a mini code block"""
    signature = str(inspect.signature(obj))
    signature = signature.replace('(', f'{obj.__name__}(\n\t', 1)
    signature = signature[::-1]
    signature = signature.replace(')', ')\n', 1)
    signature = signature[::-1]
    signature = signature.replace(', ', ',')

    for i, c in enumerate(signature):
        if c == ',' and (signature[i+1].isalpha() or signature[i+1] in '_/*'):
            signature = signature[:i] + '♪' + signature[i+1:]

    signature = signature.replace(',', ', ')
    signature = signature.replace('♪', ',\n\t')
    signature = signature.replace('\t', ' '*4)
    return ['', f"```{language}"] + signature.split('\n') + ["```", '']


def get_constant_block(__module: types.ModuleType, /, constant: str, *, language: str = "python") -> list[str]:
    """render a mini constant code block"""
    value = getattr(__module, constant)
    return ['', f"```{language}"] + [f"{constant}: {value.__class__.__name__} = {repr(value)}"] + ["```", '']


def render_block(title: str, type_: typing.Literal["Function", "Class", "Constant"], data: tuple[str, ...], file: io.TextIOWrapper, *, indent: int = 4) -> None:
    """render a block"""
    ex = ' `Internal`' if title.startswith('_') else ''
    file.write(f"!!! note \"{title} `{type_}`{ex}\"\n")
    for line in data:
        if all(c == ' ' for c in line):
            file.write("\n")
        else:
            file.write(f"{' '*indent}{line}\n")


def render_functions(__module: types.ModuleType, file: io.TextIOWrapper) -> None:
    """render functions in to Markdown file"""
    functions = tuple(filter(lambda obj: get_object_type(
        obj) == "Function", get_module_menbers(__module)))
    for i, function in enumerate(functions):
        file.write(f'### {i+1:02d}. {function.__name__}\n\n')
        data = get_code_block(function) + [getattr(function, "__doc__", "")]
        render_block(getattr(function, "__name__"), "Function", data, file)


def render_classes(__module: types.ModuleType, file: io.TextIOWrapper) -> None:
    """render classes in to Markdown file"""
    classes = tuple(filter(lambda obj: get_object_type(
        obj) == "Class", get_module_menbers(__module)))
    for i, class_ in enumerate(classes):
        file.write(f'### {i+1:02d}. {class_.__name__}\n\n')

        inheriate = '' if object in class_.__bases__ else '(' + ', '.join(
            cls.__name__ for cls in class_.__bases__) + ')'
        data = ["", getattr(class_, "__doc__", "")]

        for i, method in enumerate([class_.__init__] + list(get_class_methods(class_))):
            name = method.__name__
            ex = ' `Special`' if name.startswith(
                '__') else ' `Internal`' if name.startswith('_') else ''
            data += ['', f'!!! {'tip' if i == 0 else 'example' if name.startswith(
                '_') else 'note'} \"{name.replace('_', '\\_')} `Method`{ex}\"']
            data += [' '*4 + line for line in get_code_block(method)]
            temp = getattr(method, "__doc__", "")
            temp = [] if temp is None else temp.split('\n')
            for i, line in enumerate(temp):
                if line.startswith(' '*8):
                    temp[i] = line[4:]
                if not line.startswith(' '*4):
                    temp[i] = ' '*4 + line
            data += temp + ['']

        render_block(getattr(class_, "__name__") +
                     inheriate, "Class", data, file)


def render_constants(__module: types.ModuleType, file: io.TextIOWrapper) -> None:
    """render constants in to Markdown file"""
    raw_file = open('tkintertools/constants.py', encoding='utf-8').readlines()
    constants = tuple(c for c in get_module_data(__module)
                      if not (c.startswith('__') and c.endswith('__')))
    for constant in constants:
        data = get_constant_block(__module, constant)
        if data[-1] == "":
            data.pop()
        is_find = False
        for i, line in enumerate(raw_file):
            if not is_find:
                if line.find(constant) == -1:
                    continue
                is_find = True
            elif line.find('"') != -1:
                data += ['', raw_file[i].replace('"', ''), '']
                break
        render_block(constant, "Constant", data, file)


def render_doc(__module: types.ModuleType, *, root_path: str, const: bool = False) -> None:
    """render doc in to Markdown file"""
    name = __module.__name__.split('.')[-1]
    file = open(root_path + f"{name}.md", 'w', encoding='utf-8')
    file.write(f"{getattr(__module, "__name__")}\n")
    file.write(f'===\n')
    import_modules = [attr for attr in dir(__module) if isinstance(
        getattr(__module, attr), types.ModuleType)]
    file.write(f'\n文件描述: {getattr(__module, "__doc__", "")}  \n')
    file.write(f'外部引用: {', '.join([f'`{m}`' for m in import_modules])}  \n')
    file.write(f'源码位置: tkintertools\\{name}.py\n\n')
    if const:
        file.write("Constants - 常量\n---\n\n")
        render_constants(__module, file)
    else:
        menbers = tuple(isinstance(m, types.FunctionType)
                        for m in get_module_menbers(__module))
        if any(menbers):
            file.write("Functions - 函数\n---\n\n")
            render_functions(__module, file)
        if not all(menbers):
            file.write("Classes - 类\n---\n\n")
            render_classes(__module, file)


t = time.time()

render_doc(main, root_path='docs\\documents\\')
render_doc(exceptions, root_path='docs\\documents\\')
render_doc(tools_3d, root_path='docs\\documents\\')
render_doc(constants, root_path='docs\\documents\\', const=True)

print(time.time() - t)
