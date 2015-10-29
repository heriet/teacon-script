Teacon Script
=======

Python3 scripts for [BLACK TEA CONQUEST](http://teacon.kitunebi.com/).

see [Teacon Archive](http://heriet.info/kitunebi/teacon/archive/).

## Usage

Unzip a teacon archive file (XXX.zip) to web/archive/period2/XXX

### Convert tsv

```sh
python3 analyze_result.py web/archive/period2/XXX/RESULT > tsv/period2/XXX.tsv
```

### Report html

```sh
python3 render_report.py XXX tsv/period2/XXX.tsv web/report/period2/XXX.html
```

## License

MIT License

(c) heriet.