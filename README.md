> By contributing to this project, you agree to abide by our [Code of Conduct](https://github.com/freedomofpress/.github/blob/main/CODE_OF_CONDUCT.md).

SecureDrop is an open-source whistleblower submission system that media organizations can use to securely accept documents from, and communicate with anonymous sources. It was originally created by the late Aaron Swartz and is currently managed by the [Freedom of the Press Foundation](https://freedom.press).

This repository is used to build the [developer documentation](https://developers.securedrop.org/) for SecureDrop. Documentation for SecureDrop end users (sources, journalist and administrators) is available at https://docs.securedrop.org/ and built from https://github.com/freedomofpress/securedrop-docs.

## Quickstart

1. [Install poetry](https://python-poetry.org/docs/#installation)
2. Install the project requirements using `poetry install`
3. Run `make docs` to start a live build of the documentation at http://localhost:8000
4. Edit RST files under the docs directory - your changes will be reflected in the live build

## License

SecureDrop is open source and released under the [GNU Affero General Public License v3](/LICENSE).
