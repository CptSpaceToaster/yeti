#!/usr/bin/env python3.4
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M')

if __name__ == '__main__':
    import argparse
    _parser = argparse.ArgumentParser(description="clogger - A logger that supports colored text")
    _parser.add_argument("-f", "--log-file", dest="log_file", default="clog.log",
                         help="Example log file (default=clog.log)")
    args = _parser.parse_args()

    clog = logging.getLogger(args.log_file)
    clog.debug('debug message')
    clog.info('info message')
    clog.warn('warn message')
    clog.error('error message')
    clog.critical('critical message')
