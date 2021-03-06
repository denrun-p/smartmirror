"""Util functions used for the redis queue operations"""

import logging
import subprocess
from datetime import datetime

# Setup custom logger for upgrade
# timestamp = datetime.now().strftime('%Y_%m_%d')
# file = "./deployment/logs/{d}_redis_job.log".format(d=timestamp)
# handler = logging.FileHandler(file)
# logger = logging.getLogger("redis_logging")
# logger.setLevel(logging.INFO)
# logger.addHandler(handler)

def restart_pi_process():
    """
    Reboot the pi using the redis queue worker.
    Returns:
         output from the upgrade
    """
    cmd = "sudo reboot"
    try:
        proc = subprocess.Popen(
            "/bin/bash", shell=False, stdin=subprocess.PIPE,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        (stdout, stderr) = proc.communicate(cmd.encode("utf-8"))
        output = [stdout, stderr]
        return output
    except Exception as e:
        return e

def upgrade_pi_process():
    """
    Start a sub process to upgrade and reboot the pi.
    Logs the output to a log file in deployment/upgrade_logs

    Returns:
         output from the upgrade
    """
    cmd = "./deployment/upgrade_pi.sh"
    try:
        proc = subprocess.Popen(
            "/bin/bash", shell=False, stdin=subprocess.PIPE,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        (stdout, stderr) = proc.communicate(cmd.encode("utf-8"))

        output = [stdout, stderr]
        return output
    except Exception as e:
        return e