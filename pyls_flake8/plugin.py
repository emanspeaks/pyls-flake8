from pyls import hookimpl, lsp
import re


result_re = re.compile(r'stdin:(\d*):(\d*): (\w*) (.*)')


def results_to_diagnostic(results: str):
    diags = list()

    for line in results.splitlines():
        if line:
            linestr, col, code, msg = result_re.match(line).groups()

            lineno = int(linestr) - 1
            offset = int(col) - 1
            severity = lsp.DiagnosticSeverity.Warning

            diag = {'source': 'flake8',
                    'range': {'start': {'line': lineno, 'character': offset},
                              'end': {'line': lineno, 'character': offset + 1}
                              },
                    'code': code,
                    'message': msg,
                    'severity': severity,
                    }
            diags.append(diag)

    return diags


@hookimpl(tryfirst=True)
def pyls_lint(config, document):
    from subprocess import run, PIPE

    args = ['flake8']
    for key, val in config.plugin_settings('pyls_flake8').items():
        if key != 'enabled':
            arg = '--' + key
            if val and val is not True:
                arg += '=' + val
            args.append('--' + key)
    args.append('-')

    p = run(args, stdout=PIPE, input=document.source, text=True)

    return results_to_diagnostic(p.stdout)
