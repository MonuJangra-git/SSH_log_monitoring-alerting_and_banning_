#!/bin/bash
source "$(dirname "$0")/.env"
mutt -s "ALERT MAIL FROM SERVER" -a "$1" -- "$ALERT_EMAIL_RECIPIENT" < "$1"
