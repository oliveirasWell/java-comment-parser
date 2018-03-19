csharp = {
    'file_extensions': ['.cs'],
    'especial_characters': ['//', '/*', '*/', '"', '{', '}', '(', ')', '->', '=', ';', ',', '\n'],
    'keywords': ['abstract', 'as', 'base', 'bool',
                 'break', 'byte', 'case', 'catch',
                 'char', 'checked', 'class', 'const',
                 'continue', 'decimal', 'default', 'delegate',
                 'do', 'double', 'else', 'enum',
                 'event', 'explicit', 'extern', 'false',
                 'finally', 'fixed', 'float', 'for',
                 'foreach', 'goto', 'if', 'implicit',
                 'in', 'in', 'int', 'interface',
                 'internal', 'is', 'lock', 'long',
                 'namespace', 'new', 'null', 'object',
                 'operator', 'out', 'out', 'override',
                 'params', 'private', 'protected', 'public',
                 'readonly', 'ref', 'return', 'sbyte',
                 'sealed', 'short', 'sizeof', 'stackalloc',
                 'static', 'string', 'struct', 'switch',
                 'this', 'throw', 'true', 'try',
                 'typeof', 'uint', 'ulong', 'unchecked',
                 'unsafe', 'ushort', 'using', 'using', 'static',
                 'virtual', 'void', 'volatile', 'while', ],
    'objetc_orientation': True,
    'strict_objetc_orientation': False,
    'has_lambda': False,
    'repos': [['https://github.com/shadowsocks/shadowsocks-windows', 'shadowsocks-windows'],
              ['https://github.com/CodeHubApp/CodeHub', 'CodeHub'],
              ['https://github.com/dotnet/corefx', 'corefx'],
              ['https://github.com/PowerShell/PowerShell', 'PowerShell'],
              ['https://github.com/dotnet/coreclr', 'coreclr'],
              ['https://github.com/dotnet/roslyn', 'roslyn'], ]
}

java = {
    'file_extensions': ['.java'],
    'especial_characters': ['//', '/*', '*/', '"', '{', '}', '(', ')', '->', '=', ';', ',', '\n'],
    'keywords': [
        'abstract', 'continue', 'for', 'new', 'switch', 'assert', 'default',
        'goto', 'package', 'synchronized', 'boolean', 'do', 'if', 'private',
        'this', 'break', 'double', 'implements', 'protected', 'throw', 'byte',
        'else', 'import', 'public', 'throws', 'case', 'enum', 'instanceof	return',
        'transient', 'catch', 'extends', 'int', 'short', 'try',
        'char', 'final', 'interface', 'static', 'void', 'class', 'finally',
        'long', 'strictfp', 'volatile', 'const', 'float	native', 'super', 'while'
    ],
    'objetc_orientation': False,
    'strict_objetc_orientation': True,
    'has_lambda': True,
    'repos': [
        # github_path, folder_name
        ['https://github.com/ReactiveX/RxJava', 'RxJava'],
        ['https://github.com/elastic/elasticsearch', 'elasticsearch'],
        ['https://github.com/square/retrofit', 'retrofit'],
        ['https://github.com/google/guava', 'guava'],
        ['https://github.com/spring-projects/spring-boot', 'spring-boot'],
        ['https://github.com/PhilJay/MPAndroidChart', 'MPAndroidChart'],
    ],
}

javaScript = {
    'file_extensions': ['.js'],
    'especial_characters': ['//', '/*', '*/', '"', '{', '}', '(', ')', '->', '=', ';', ',', '\n'],
    'keywords': [
        'abstract', 'arguments', 'await*', 'boolean',
        'break', 'byte', 'case', 'catch',
        'char', 'class*', 'const', 'continue',
        'debugger', 'default', 'delete', 'do',
        'double', 'else', 'enum*', 'eval',
        'export*', 'extends*', 'false', 'final',
        'finally', 'float', 'for', 'function',
        'goto', 'if', 'implements', 'import*',
        'in', 'instanceof', 'int', 'interface',
        'let*', 'long', 'native', 'new',
        'null', 'package', 'private', 'protected',
        'public', 'return', 'short', 'static',
        'super*', 'switch', 'synchronized', 'this',
        'throw', 'throws', 'transient', 'true',
        'try', 'typeof', 'var', 'void',
        'volatile', 'while', 'with', 'yield',
    ],
    'objetc_orientation': True,
    'strict_objetc_orientation': False,
    'has_lambda': True,
    'spagget_code': True,
    'repos': [
        ['https://github.com/d3/d3', 'd3'],
        ['https://github.com/vuejs/vue', 'vue'],
        ['https://github.com/freeCodeCamp/freeCodeCamp', 'freeCodeCamp'],
        ['https://github.com/facebook/react-native', 'react-native'],
        ['https://github.com/angular/angular.js', 'angular.js'],
        ['https://github.com/airbnb/javascript', 'javascript'],
    ]
}

shellscript = {
    'file_extensions': ['.shell', 'sh'],
    'especial_characters': ['//', '/*', '*/', '"', '{', '}', '(', ')', '->', '=', ';', ',', '\n'],
    'keywords': ['if', 'else', 'elif', 'then', 'fi', 'case', 'esac',
                 'for', 'select', 'while', 'until', 'do', 'done', 'in',
                 'function', 'time', '{', '}', '!', '[[', ']]', 'coproc'],
    'objetc_orientation': False,
    'strict_objetc_orientation': False,
    'has_lambda': False,
}


cplusplus = {
    'file_extension': ['.c', '.cpp', '.h'],
}