import json
import os
import sys
import csv
import inspect
import types
from os.path import join

DEFAULT_JSON_OUTPUT = 'global-counter.json'

g_counter = 0
functionsDictionary = dict()
functionCallsStack = []
first_function_flag = True


# Simple structure to capture counts for module/method
# in the instrumented program.
class GlobalCounter:

    def __init__(self):
        # self.counter = 0
        self.data = {}

    @staticmethod
    def trace_calls(frame, event, arg):
        #if event != 'call':
        #   return
        co = frame.f_code
        func_name = co.co_name
        #if func_name == 'write':
            # Ignore write() calls from print statements
        #    return
        func_line_no = frame.f_lineno
        func_filename = co.co_filename
        caller = frame.f_back
        caller_line_no = caller.f_lineno
        caller_filename = caller.f_code.co_filename
        GlobalCounter.update_counters(func_name)
        print 'Call to %s on line %s of %s from line %s of %s' % \
              (func_name, func_line_no, func_filename,
               caller_line_no, caller_filename)
        # print "current counter value is: ", counter
        #print 'number of functions before and now', temp, g_counter
        #print 'Difference number of functions: ', g_counter-temp
        return

    @staticmethod
    def update_counters(func_name):
        global g_counter
        global functionsDictionary
        g_counter += 1
        functionsDictionary[func_name] = functionsDictionary.get(func_name, 0) + 1

    @staticmethod
    def init_tracer():
        sys.settrace(GlobalCounter.trace_calls)

    @staticmethod
    def fqn(class_name, method, lineno):
        print 'CURRENT COUNTER AT FUNCTION BEGINNING: ', g_counter
        name = method + ':' + str(lineno)
        if class_name and class_name != 'None':
            name = class_name + '::' + name
        return name

    def count(self, file, class_name=None, method=None, lineno=-1):
        if file not in self.data:
            self.data[file] = {}
        d = self.data[file]
        name = GlobalCounter.fqn(class_name, method, lineno)
        print 'THIS IS THE END OF THE FUNCTION'
        #global g_counter
        #global functionCallsStack
        #functionCallsStack.append(g_counter)
        #print 'Stacked counter is: ', functionCallsStack[-1]
        if name not in d:
            d[name] = 0
        d[name] += 1
        GlobalCounter.print_difference(name)
        GlobalCounter.push_current_counte_wo_check()

    def to_json(self, file_location=DEFAULT_JSON_OUTPUT):
        print "Writing to %s" % file_location
        #print "current counter value is: "
        try:
            fd = open(file_location, 'w')
            json.dump(self.data, fd, indent=2, sort_keys=True)
            fd.close()
        except Exception, ex:
            print "Serialization error:", str(ex)

    @staticmethod
    def to_csv():
        print "Writing to CSV"
        with open('messages.csv', 'w') as f:
            for functionName in functionsDictionary:
                f.write("%s,%s\n" % (functionName, functionsDictionary[functionName]))

    @staticmethod
    def print_global_counter():
        print "global counter is: ", g_counter
        print "the functions executed and times are: ", functionsDictionary

    @staticmethod
    def print_difference(method_name):
        print 'THE MESSAGE DIFFERENCE BEFORE AND AFTER', method_name, ' IS: ', g_counter-functionCallsStack.pop()

    @staticmethod
    def push_current_counter():
        global first_function_flag
        if first_function_flag:
            first_function_flag = False
            return
        functionCallsStack.append(g_counter)
        print 'Stacked counter is: ', functionCallsStack[-1]

    @staticmethod
    def initialize_call_stack():
        functionCallsStack.append(0)

    @staticmethod
    def check_if_function_has_been_called():
        print 'testing this '

    @staticmethod
    def push_current_counte_wo_check():
        functionCallsStack.append(g_counter)

GlobalCounterInst = GlobalCounter()
