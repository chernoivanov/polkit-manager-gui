import syslog


def message_syslog(message: str) -> None:
    """
    Writes message to syslog with level of INFO
    """
    syslog.openlog("polkit-manager-gui")
    syslog.syslog(syslog.LOG_INFO, message)
    syslog.closelog()
