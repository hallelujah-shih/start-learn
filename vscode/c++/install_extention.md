# 插件安装记录
```
初始化环境安装插件
```
## clang-format
```
统一编码格式的争论，参见go-format

> ext install xaver.clang-format
> clang-format -style=Google -dump-config > .clang-format
并在settings中设置了
    "editor.formatOnSave": true
    "C_Cpp.clang_format_style": "file"
    "C_Cpp.clang_format_sortIncludes": true
```

## c/c++
```
> ext install ms-vscode.cpptools
settings存在一系列的default设置
    C_Cpp.default.includePath                          : string[]
    C_Cpp.default.defines                              : string[]
    C_Cpp.default.compileCommands                      : string
    C_Cpp.default.macFrameworkPath                     : string[]
    C_Cpp.default.forcedIncludes                       : string[]
    C_Cpp.default.intelliSenseMode                     : string
    C_Cpp.default.compilerPath                         : string
    C_Cpp.default.cStandard                            : c89 | c99 | c11
    C_Cpp.default.cppStandard                          : c++98 | c++03 | c++11 | c++14 | c++17
    C_Cpp.default.browse.path                          : string[]
    C_Cpp.default.browse.databaseFilename              : string
    C_Cpp.default.browse.limitSymbolsToIncludedHeaders : boolean

*** 使用clang command adapter，设置了如下配置
    "C_Cpp.intelliSenseEngine": "Default"
    "C_Cpp.autocomplete": "Disabled"
    "C_Cpp.errorSquiggles": "Disabled"
    "C_Cpp.formatting": "Disabled"

补全：
> ext install mitaki28.vscode-clang
手动改了一些配置
    "clang.completion.enable": true,
    "clang.diagnostic.enable": true,
    "clang.completion.maxBuffer": 209715200,
    "clang.diagnostic.maxBuffer": 2621440,
    "clang.diagnostic.delay": 100
```

## REF
    [cpp-tools-settings](https://github.com/Microsoft/vscode-cpptools/blob/master/Documentation/LanguageServer/Customizing%20Default%20Settings.md)
    [clang-format](https://marketplace.visualstudio.com/items?itemName=xaver.clang-format)
    [clang-format style options](https://clang.llvm.org/docs/ClangFormatStyleOptions.html)
    [c/c++](https://marketplace.visoualstudio.com/items?itemName=ms-vscode.cpptools)
    [c/c++ clang command adapter](https://marketplace.visualstudio.com/items?itemName=mitaki28.vscode-clang)
    [Visual Studio Code如何编写运行C、C++？](https://www.zhihu.com/question/30315894)
