import subprocess
import re
import logging
from datetime import datetime
logger = logging.getLogger(__name__.split('.')[0])

class TimeDateInfo:
    """
    A class to represent the time and date information of a system.
    """
    """
                Local time: Mon 2025-05-19 15:19:33 EEST
            Universal time: Mon 2025-05-19 12:19:33 UTC
                    RTC time: Mon 2025-05-19 12:19:33
                    Time zone: Europe/Kiev (EEST, +0300)
    System clock synchronized: no
                NTP service: n/a
            RTC in local TZ: no
    """
    tz_token_specification = [
        ('TIMEZONE', r'Time zone: (?P<TZ_NAME>\S+) \((?P<TZ_ABBR>\S+)'\
            ', (?P<TZ_OFFSET>\S+)\)'),
        ('LOCAL_TIME', r'Local time: (?P<TZ_LOCAL_TIME>.+)'),
        ('UNIVERSAL_TIME', r'Universal time: (?P<TZ_UNIVERSAL_TIME>.+)'),
        ('RTC_TIME', r'RTC time: (?P<TZ_RTC_TIME>.+)'),
        ('SYSTEM_CLOCK_SYNC', r'System clock synchronized: (?P<TZ_SYSTEM_CLOCK_SYNC>\S+)'),
        ('NTP_SERVICE', r'NTP service: (?P<TZ_NTP_SERVICE>\S+)'),
        ('RTC_LOCAL', r'RTC in local TZ: (?P<TZ_RTC_LOCAL>\S+)')
        # ('TIMEZONE', r'Time zone: (?P<TZ_NAME>.+)')
    ]
    tz_tok_regex = '|'.join('(?P<%s>%s)' % pair\
                                        for pair in tz_token_specification)

    def __init__(self):
        """
        Initialize the TimeDateInfo object with the given parameters.

        :param local_time: The local time of the system.
        :param universal_time: The universal time (UTC) of the system.
        :param rtc_time: The RTC (Real-Time Clock) time of the system.
        :param time_zone: The time zone of the system.
        :param ntp_enabled: Whether NTP (Network Time Protocol) is enabled or not.
        """
        # self.local_time = local_time
        # self.universal_time = universal_time
        # self.rtc_time = rtc_time
        # self.time_zone = time_zone
        # self.ntp_enabled = ntp_enabled


    def __str__(self):
        """
        Return a string representation of the TimeDateInfo object.
        """
        return f"Local Time: {self.local_time}, Universal Time: {self.universal_time}, " \
               f"RTC Time: {self.rtc_time}, Time Zone: {self.time_zone}, NTP Enabled: {self.ntp_enabled}"
    
    def __repr__(self):
        """
        Return a string representation of the TimeDateInfo object for debugging.
        """
        return f"TimeDateInfo(local_time={self.local_time}, universal_time={self.universal_time}, " \
               f"rtc_time={self.rtc_time}, time_zone={self.time_zone}, ntp_enabled={self.ntp_enabled})"
    
    def to_dict(self):
        """
        Convert the TimeDateInfo object to a dictionary representation.
        """
        return {
            "local_time": self.local_time,
            "universal_time": self.universal_time,
            "rtc_time": self.rtc_time,
            "time_zone": self.time_zone,
            "ntp_enabled": self.ntp_enabled
        }

    @classmethod
    def parse_timedatectl_output(cls, cmd_output):
        """
        Parse the output of the 'timedatectl' command and extract relevant information.

        :param cmd_output: The output of the 'timedatectl' command as a string.
                           result = subprocess.run(['timedatectl'], stdout=subprocess.PIPE)
                           cmd_output = result.stdout.decode('utf-8')
        :return: A dictionary containing the parsed information.
        """

        result_dict = {
            "timezone" : "None",
            "timezone_c" : "None",
        }
        tz_name = ""
        tz_abbr = ""
        tz_offset = ""
        logger.info("Run timedatectl...")
        # result = subprocess.run(['timedatectl'], stdout=subprocess.PIPE)
        # for mo in re.finditer(cls.tz_tok_regex,\
        #                                         result.stdout.decode('utf-8')):
        for mo in re.finditer(cls.tz_tok_regex, cmd_output):
            kind = mo.lastgroup
            value = mo.group()
            if kind == 'TIMEZONE':
                tz_name = mo.group('TZ_NAME')
                tz_abbr = mo.group('TZ_ABBR')
                tz_offset = mo.group('TZ_OFFSET')
                result = tz_name + ' (' + tz_abbr + ', ' + tz_offset + ')'
                result_dict['timezone_c'] = result
                if tz_name != 'Custom': 
                    result_dict['timezone'] = tz_name
            elif kind == 'LOCAL_TIME':
                local_time = mo.group('TZ_LOCAL_TIME')
                local_time = local_time.strip()
                result_dict['local_time'] = datetime.strptime(local_time, '%a %Y-%m-%d %H:%M:%S %Z').strftime('%Y-%m-%d %H:%M:%S')
            elif kind == 'UNIVERSAL_TIME':
                universal_time = mo.group('TZ_UNIVERSAL_TIME')
                universal_time = universal_time.strip()
                result_dict['universal_time'] = datetime.strptime(universal_time, '%a %Y-%m-%d %H:%M:%S %Z').strftime('%Y-%m-%d %H:%M:%S')
            elif kind == 'RTC_TIME':
                rtc_time = mo.group('TZ_RTC_TIME')
                rtc_time = rtc_time.strip()
                result_dict['rtc_time'] = datetime.strptime(rtc_time, '%a %Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
            elif kind == 'SYSTEM_CLOCK_SYNC':
                sync_status = mo.group('TZ_SYSTEM_CLOCK_SYNC')
                sync_status = sync_status.strip()
                result_dict['system_clock_sync'] = sync_status
            elif kind == 'NTP_SERVICE':
                ntp_service = mo.group('TZ_NTP_SERVICE')
                ntp_service = ntp_service.strip()
                result_dict['ntp_service'] = ntp_service
            elif kind == 'RTC_LOCAL':
                rtc_local_tz = mo.group('TZ_RTC_LOCAL')
                rtc_local_tz = rtc_local_tz.strip()
                result_dict['rtc_local_tz'] = rtc_local_tz
        return result_dict
