import re

from pylsp import hookimpl, lsp

# default ignored by Flake8 package:
# E121, continuation line under-indented for hanging indent
# E123, closing bracket does not match indentation of opening bracket’s line
# E126, continuation line over-indented for hanging indent
# E226, missing whitespace around arithmetic operator
# E241, multiple spaces after ‘,’
# E242, tab after ‘,’
# E704, multiple statements on one line (def)

result_re = re.compile(r"stdin:(\d*):(\d*): (\w*) (.*)")

# default flake messages to error except these
flake_warnings = (
    "F401",  # module imported but unused
    "F402",  # import module from line N shadowed by
    #   loop variable
    "F403",  # ‘from module import *’ used;
    #   unable to detect undefined names
    "F404",  # future import(s) name after other statements
    "F405",  # name may be undefined, or defined from
    #   star imports: module
    "F602",  # dictionary key variable name repeated with
    #   different values
    "F841",  # local variable name is assigned to but never used
)

# default code style messages to warnings except these
style_errors = (
    "E112",  # expected an indented block
    "E113",  # unexpected indentation
    "E741",  # do not use variables named ‘l’, ‘O’, or ‘I’
    "E742",  # do not define classes named ‘l’, ‘O’, or ‘I’
    "E743",  # do not define functions named ‘l’, ‘O’, or ‘I’
    "E901",  # SyntaxError or IndentationError
    "E902",  # IOError
    "E999",  # invalid syntax
)

severity_enum = lsp.DiagnosticSeverity
warning = severity_enum.Warning
error = severity_enum.Error


def results_to_diagnostic(results: str, document):
    diaglist = list()
    for line in results.splitlines():
        if line:
            linestr, col, code, msg = result_re.match(line).groups()

            lineno = int(linestr) - 1
            offset = int(col) - 1

            if (
                code[0] == "F" and code not in flake_warnings
            ) or code in style_errors:
                severity = error
            else:
                severity = warning

            start_mark = {"line": lineno, "character": offset}
            end_mark = {"line": lineno, "character": offset + 1}
            if document:
                word = document.word_at_position(start_mark)
                if word:
                    end_mark["character"] = start_mark["character"] + len(word)

            diag = {
                "source": "flake8",
                "range": {"start": start_mark, "end": end_mark},
                "code": code,
                "message": msg,
                "severity": severity,
            }
            diaglist.append(diag)

    return diaglist


def return_error(stderr: str):
    return [
        {
            "source": "flake8",
            "range": {
                "start": {"line": 0, "character": 0},
                "end": {"line": 0, "character": 1},
            },
            "code": "ERR",
            "message": stderr,
            "severity": error,
        }
    ]


camelcase_snakecase_mapping = {
    "maxLineLength": "max-line-length",
    "hangClosing": "hang-closing",
    "perFileIgnores": "per-file-ignores",
    "extendIgnore": "extend-ignore",
}


def to_snake_case(option):
    if option in camelcase_snakecase_mapping:
        return camelcase_snakecase_mapping[option]

    return option


def compile_flake8_args(config):
    args = ["flake8"]
    for key, val in config.plugin_settings("flake8").items():
        if key == "enabled":
            continue

        key = to_snake_case(key)
        arg = "--" + key

        if val is None:
            continue

        if isinstance(val, list):
            val = ",".join(val)
            arg += f"={val}"
        elif isinstance(val, bool):
            if not val:
                continue
        else:
            arg += f"={val}"

        args.append(arg)
    args.append("-")
    return args


def run_flake8(args, document):
    from subprocess import PIPE, run

    return run(args, stdout=PIPE, stderr=PIPE, input=document.source.encode())


@hookimpl(tryfirst=True)
def pylsp_lint(config, document):
    args = compile_flake8_args(config)
    p = run_flake8(args, document)
    stderr = p.stderr.decode()
    if stderr:
        return return_error(stderr)
    return results_to_diagnostic(p.stdout.decode(), document)


@hookimpl
def pylsp_settings():
    """
    Disable all plugins which are supported by flake8
    """
    config = {
        "plugins": {
            "pycodestyle": {"enabled": False},
            "mccabe": {"enabled": False},
            "pyflakes": {"enabled": False},
        }
    }
    return config


if __name__ == "__main__":

    class test_document:
        def __init__(self, src: str):
            self.source = src

    class test_config:
        def plugin_settings(self, plugin: str) -> dict:
            return {"extend-ignore": "W503"}

    testdoc = test_document("import sys \nx.y()")
    testcfg = test_config()

    args = compile_flake8_args(testcfg)
    print(args)
    p = run_flake8(args, testdoc)
    err = p.stderr.decode()
    if err:
        print("stderr: " + repr(return_error(err)))
    res = p.stdout.decode()
    print(res)
    diag = results_to_diagnostic(res)
    print(diag)
