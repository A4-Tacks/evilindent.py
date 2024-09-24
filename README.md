This script will randomly your indentation block space count

## Examples

**test.py**

```python
def run_file(file, out_file) -> None:
    prev_indent = 0
    indent_map = [""]
    for line in file:
        indent, solid = get_indent(line)

        if indent or solid:
            if indent+1 > len(indent_map):
                new_indent = (len(indent_map[prev_indent])
                              + randrange(max_indent) + 1)
                set_list(indent_map, indent, " " * new_indent)

            if indent:
                indent_map[indent+1:] = ()

            prev_indent = indent
        print(indent_map[indent], end=solid, file=out_file)
```

```python
$ python evilindent.py -h
Usage: evilindent [Option...] [FILE...]
Randomly indent block
Warning: This may damage multiple lines string, etc

Option:
    -i, --in-place      edit files in place
    -b, --backup=<SUFFIX>
                        in place and makes backup
    -m, --max-indent=<NUM>
                        max indent spaces
    -t, --tab           use tab indent
    -h, --help          show this help
    -v, --version       show version

FILE:
    -                   input from stdin
$ python evilindent.py test.py
def run_file(file, out_file) -> None:
   prev_indent = 0
   indent_map = [""]
   for line in file:
           indent, solid = get_indent(line)

           if indent or solid:
             if indent+1 > len(indent_map):
                         new_indent = (len(indent_map[prev_indent])
                                 + randrange(max_indent) + 1)
                         set_list(indent_map, indent, " " * new_indent)

             if indent:
                indent_map[indent+1:] = ()

             prev_indent = indent
           print(indent_map[indent], end=solid, file=out_file)
```
