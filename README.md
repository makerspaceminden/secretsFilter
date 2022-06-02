# Secrets filter
Very basic secrets filter (e.g. for API Keys or passwords). Uses simple string replacing functions.

## Usage
### Command line:
```
MSM Secrets filter Program to filter out any API keys, passwords and other
secrets. Replaces them with a defined string e.g. {APIKey}

optional arguments:
  -h, --help            show this help message and exit
  -f FILTERFILE, --filter FILTERFILE
                        JSON File containing an array of name: secret mapping:
                        Example: {"WifiPassword": "01234567"}
  -s SCANDIR, --scanDir SCANDIR
                        Directory where files should be scanned for the names
                        / secrets
  -d DELIMITERS, --delimiters DELIMITERS
                        Delimiters for the string replacing, separated by ","
                        Can be used to fit this program for enviroments,
                        Examples: -d "," --> in code as a String: "APIKey" -d
                        /*,*/ --> in code as a comment: /*APIKey*/
  -r, --reverseMode     Undoes filtering as long as the same json is used
                        ("filters" in reverse)
  -v, --verbose         Does verbose logging
```

### Module:
First create a new KeyFilter object:
```
import keyFilter
filter = keyFilter.KeyFilter(mappingObject, scanDir, preDelimiter, postDelimiter, isVerbose, doReverse)
```
 - mappingObject: Dict containing the name->secret mapping
 - scanDirPath: Path to the directory where the scan should be performed. overwrites files in there, so write rights are required.
 - preDelimiter: Delimiter used in replacing the secret keys. Prepended before the name.
 - postDelimiter: Delimiter used in replacing the secret keys. Appended after the name.
 - isVerbose: Do logging on stdout
 - doReverse: Reverses the process, replaces delimiters+name with secret (instead of secret->delimiters+name)

Filtering is then done via the applyFilter-function:
```
filter.applyFilter()
```