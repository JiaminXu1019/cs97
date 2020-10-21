#!/usr/bin/env python3
"""
Shuffles its input by outputting a random permutation of its input lines. Each output permutation is equally likely
$Id: shuf.py,v 1.0 2020/04/14 13:05:43 amy Exp $
"""

import random, sys
import argparse

class shuf:
    def __init__(self, filename, numlines):
        try:
            f = open(filename, 'r')
            self.lines = f.readlines()
            f.close()
        except:
            self.lines=filename
        self.numlines = numlines
 
    def randomsample(self):
        return random.sample(self.lines, self.numlines)

    def randomrepeat(self):
        return random.choice(self.lines)
    
def main():

    parser = argparse.ArgumentParser(description="Shuffles its input by outputting a random permutation of its input lines. Each output permutation is equally likely.")
                      
    parser.add_argument("-e", "--echo",
                        dest="echo_args", nargs='*',
                      help="Treat each ARG as an input line")

    parser.add_argument("-n", "--head-count",
                        action="store", dest="count",type=int,
                      help="Output at most count lines. By default, all input lines are output.")

    parser.add_argument("-r", "--repeat", action="store_const", dest="rep", default=False, const=True,
                      help="Repeat output values, that is, select with replacement. With this option the output is not a permutation of the input; instead, each output line is randomly chosen from all the inputs. This option is typically combined with --head-count; if --head-count is not given, shuf repeats indefinitely.")

    parser.add_argument("-", action="store_true", dest="get", help="Get input from standard input")
    
    options, args = parser.parse_known_args()
    numlines = None
    try:
        numlines = int(options.count)
        if len(args) == 1:
            input_file = args[0]
        elif options.echo_args is not None and len(args) > 1:
            input_file = args
        else:
            parser.error("extra operand: '{0}'".format(args[1]))
    except Exception:
        try:
            input_file=options.echo_args
            if numlines is None:
                numlines=len(options.echo_args)
        except:
            try:
                input_file = args[0]
                with open(args[0]) as my_file:
                    numlines=(sum(1 for _ in my_file))
            except:
               try:
                   parser.error("{0}: no such file or directory".format(args[0]))
                   sys.exit(1)
               except Exception:
                    input_file = []
                    for line in sys.stdin:
                        input_file.append(line)
                    if numlines is None:
                        numlines = len(input_file)
                                            
    if numlines < 0:
        parser.error("invalid line count: '{0}'".
                     format(options.count))
    if numlines > len(input_file):
        numlines = len(input_file)
        
    try:
        generator = shuf(input_file, numlines)
        random_sample = generator.randomsample()
        if options.count is None and options.rep:
            while True:
                sys.stdout.write(generator.randomrepeat())
        elif options.count is not None and options.rep:
            for i in range (options.count):
                sys.stdout.write(generator.randomrepeat())
        else:
            for i in range (len(random_sample)):
                random_sample[i]=random_sample[i].strip('\n')
                sys.stdout.write(random_sample[i]+'\n')
            
    except IOError as err:
        parser.error("I/O error({0}): {1}".
                     format(err.errno, err.strerror))

if __name__ == "__main__":
    main()
