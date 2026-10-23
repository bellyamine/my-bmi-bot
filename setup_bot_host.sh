#!/bin/sh
set -eu

project_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
python=$(command -v python3) || {
    printf 'Error: python3 was not found.\n' >&2
    exit 1
}
config_dir="${HOME}/.config/bmi-bot"
unit_dir="${HOME}/.config/systemd/user"
token_file="${config_dir}/token.env"
unit_file="${unit_dir}/bmi-bot.service"

if ! "$python" -c 'import telebot' >/dev/null 2>&1; then
    printf 'Error: pyTelegramBotAPI is not installed for %s.\n' "$python" >&2
    printf 'Install it with: %s -m pip install pyTelegramBotAPI\n' "$python" >&2
    exit 1
fi

if ! systemctl --user is-system-running >/dev/null 2>&1; then
    printf 'Error: the user systemd service manager is unavailable.\n' >&2
    exit 1
fi

printf 'Enter the new Telegram bot token (input is hidden): '
stty -echo
trap 'stty echo 2>/dev/null || true' EXIT HUP INT TERM
IFS= read -r token
stty echo
trap - EXIT HUP INT TERM
printf '\n'

if [ -z "$token" ]; then
    printf 'Error: the token cannot be empty.\n' >&2
    exit 1
fi

case "$token" in
    *[!A-Za-z0-9:_-]*)
        printf 'Error: the token contains unsupported characters.\n' >&2
        exit 1
        ;;
esac

umask 077
mkdir -p "$config_dir" "$unit_dir"
printf 'TELEGRAM_BOT_TOKEN=%s\n' "$token" > "$token_file"
unset token

cat > "$unit_file" <<EOF
[Unit]
Description=BMI Telegram bot
After=network-online.target

[Service]
Type=simple
WorkingDirectory=${project_dir}
EnvironmentFile=${token_file}
ExecStart=${python} ${project_dir}/bmi_bot.py
Restart=on-failure
RestartSec=10

[Install]
WantedBy=default.target
EOF

systemctl --user daemon-reload
systemctl --user enable --now bmi-bot.service
systemctl --user --no-pager --full status bmi-bot.service

printf '\nBot service installed. It starts when your user session starts.\n'
