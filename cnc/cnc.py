#!/usr/bin/env python3


import argparse
import re
import subprocess
import time


from gsmmodem.modem import GsmModem


def get_time_from_modem(modem):
    result, success = modem.write('AT+CCLK?')
    p = re.compile('^\+CCLK: "(\d\d)/(\d\d)/(\d\d),(\d\d):(\d\d):(\d\d)"$')
    m = p.match(result)
    year = int(m.group(1))
    if year >= 80:
        year += 1900
    else:
        year += 2000
    month = int(m.group(2))
    day = int(m.group(3))
    hour = int(m.group(4))
    minute = int(m.group(5))
    seconds = int(m.group(6))
    result = "%04d-%02d-%02d %02d:%02d:%02d" % (year, month, day, hour, minute, seconds)
    return result


class Command:

    def __init__(self, text):
        self.process = subprocess.run(text, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        self.stdout = self.process.stdout
        self.stderr = self.process.stderr
        self.returncode = self.process.returncode
        print("Command returned '{}' for '{}'\nStdout:\n{}\nStderr:\n{}".format(self.process.returncode, text, self.process.stdout, self.process.stderr))


class NoPppDefaultRouteException(Exception):
    pass


class NoConnectivityException(Exception):
    pass


class App:

    REBOOT_TIMER_MINUTES = 10
    PPP_SETUP_GRACE_TIME_SECONDS = 60
    PING_GRACE_TIME_SECONDS = 60
    PING_TARGET = "8.8.8.8" # google dns

    def __init__(self, modem_device, modem_baud, modem_pin, ppp_provider, ppp_interface, phone_number_override):
        self._pon_requested = False
        self._modem_device = modem_device
        self._modem_baud = modem_baud
        self._modem_pin = modem_pin
        self._ppp_provider = ppp_provider
        self._ppp_interface = ppp_interface
        self._phone_number_override = phone_number_override


    def _handleSms(self, sms):
        # override phone number if requested
        sms.number = self._phone_number_override or sms.number

        #handle messages
        if sms.text.startswith('!'):
            command = sms.text[1:]
            print(command)
            process = Command(command)
            sms.reply("Result: {}\n{}\n{}".format(process.returncode, process.stdout, process.stderr))

        elif sms.text == 'setclock':
            timestamp_utc = get_time_from_modem(sms.getModem())
            # set clock only if recent
            if timestamp_utc.startswith("20"):
                sms.reply('Setting clock to UTC timestamp {} ...'.format(timestamp_utc))
                process = Command("sudo date -u -s '{}'".format(timestamp_utc))
                sms.reply("Result: {}\n{}\n{}".format(process.returncode, process.stdout, process.stderr))
            else:
                sms.reply('Result: timestamp {} is too old'.format(timestamp_utc))

        elif sms.text == 'pon':
            self._pon_requested = True
            # plan reboot in case connection is broken
            process = Command("sudo shutdown -r +{} 'cnc plans a safe reboot'".format(self.REBOOT_TIMER_MINUTES))
            sms.reply("Result: setting pon flag and planning reset in {} minutes, which returned {} with stdout:\n{}\n and stderr:\n {}".format(self.REBOOT_TIMER_MINUTES, process.returncode, process.stdout, process.stderr))
            # if reboot cannot be planned, cancel bringing connection
            if process.returncode != 0:
                self._pon_requested = False


    def process_sms(self):
        self._pon_requested = False
        # handle SMS
        modem = GsmModem(self._modem_device, self._modem_baud, smsReceivedCallbackFunc=self._handleSms)
        modem.connect(self._modem_pin)
        modem.smsTextMode = False
        modem.processStoredSms()
        try:
            modem.rxThread.join(1)
        finally:
            modem.close()


    def _wait_for_default_route_via_ppp(self):
        for i in range(self.PPP_SETUP_GRACE_TIME_SECONDS):
            process = Command("ip route")
            if process.returncode != 0:
                raise NoPppDefaultRouteException()
            # search for appropriate default route entry
            r = re.compile('default\s+dev\s+{}'.format(self._ppp_interface))
            for route in process.stdout.splitlines():
                if r.match(route):
                    return
            time.sleep(1)
        raise NoPppDefaultRouteException()


    def _start_ppp(self):
        process = Command("sudo pon {}".format(self._ppp_provider))
        if process.returncode != 0:
            self._stop_ppp()


    def _stop_ppp(self):
        process = Command("sudo poff {}".format(self._ppp_provider))


    def _wait_for_icmp_connectivity(self):
        for i in range(self.PING_GRACE_TIME_SECONDS):
            process = Command("ping -w 3 -i 1 {}".format(self.PING_TARGET))
            if process.returncode == 0:
                return
            time.sleep(1)
        raise NoConnectivityException()


    def setup_connection(self):
        # initiate modem connection
        self._start_ppp()
        # wait check for default route
        try:
            self._wait_for_default_route_via_ppp()
        except NoPppDefaultRouteException:
            print("no default route found, stopping pppd and exiting")
            self._stop_ppp()
            return
        # check for real connectivity
        try:
            self._wait_for_icmp_connectivity()
        except NoConnectivityException:
            print("no internet connectivity, stopping pppd and exiting")
            self._stop_ppp()
            return
        # TODO: initiate VPN


    def run(self):
        self.process_sms()
        if self._pon_requested:
            self._pon_requested = False
            self.setup_connection()


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("modem_device")
    parser.add_argument("--baud", default=115200)
    parser.add_argument("--pin", default=None)
    parser.add_argument("--phone-number-override", default=None)

    parser.add_argument("ppp_provider")
    parser.add_argument("ppp_interface")
    args = parser.parse_args()

    app = App(args.modem_device, args.baud, args.pin, args.ppp_provider, args.ppp_interface, args.phone_number_override)
    app.run()


if __name__ == '__main__':
    main()
