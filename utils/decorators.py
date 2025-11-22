#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
Message Decorators for VIPBOMBER-V2
"""

import sys
import time
from colorama import Fore, Style, init

# Initialize colorama
init()

class MessageDecorator:
    def __init__(self, mode="icon"):
        self.mode = mode
        self.colors = {
            'success': Fore.GREEN,
            'error': Fore.RED,
            'warning': Fore.YELLOW,
            'info': Fore.CYAN,
            'command': Fore.MAGENTA,
            'section': Fore.BLUE
        }
    
    def _format_message(self, message_type, message):
        icons = {
            'success': '[✓]',
            'error': '[✗]',
            'warning': '[!]',
            'info': '[i]',
            'command': '[>]',
            'section': '[#]'
        }
        
        if self.mode == "stat":
            return f"{message}"
        else:
            icon = icons.get(message_type, '[ ]')
            color = self.colors.get(message_type, Fore.WHITE)
            return f"{color}{icon} {message}{Style.RESET_ALL}"
    
    def SuccessMessage(self, message):
        print(self._format_message('success', message))
    
    def FailureMessage(self, message):
        print(self._format_message('error', message))
    
    def WarningMessage(self, message):
        print(self._format_message('warning', message))
    
    def GeneralMessage(self, message):
        print(self._format_message('info', message))
    
    def CommandMessage(self, message):
        return self._format_message('command', message)
    
    def SectionMessage(self, message):
        print(self._format_message('section', message))