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
```

## REF
    [cpp-tools-settings](https://github.com/Microsoft/vscode-cpptools/blob/master/Documentation/LanguageServer/Customizing%20Default%20Settings.md)
    [clang-format](https://marketplace.visualstudio.com/items?itemName=xaver.clang-format)
    [clang-format style options](https://clang.llvm.org/docs/ClangFormatStyleOptions.html)
    [c/c++](https://marketplace.visualstudio.com/items?itemName=ms-vscode.cpptools)
