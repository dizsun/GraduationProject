# coding=UTF-8
import base64
import MySQLdb
from APKManager import APKManager



f = open('regression_test')
l = f.readline()
f.close()
f = open('regression_test', 'w')
f.write(l.replace('gate', '\ngate'))
f.close()
