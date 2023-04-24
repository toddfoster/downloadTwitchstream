#!/bin/bash
set -e
#
# postProcess.bash: Fix up videos downloaded from twitch
# 1. rename, changing timestamp to local time
# 2. encode video with libx265
# 3. copy to final resting place
# 4. move original to trash (where I can find it if something went wrong)
#

_self="${0##*/}"

#DEBUG="true"
report() {
	printf "LOG $(date --iso-8601=seconds) | $_self | $*\n"
}

SOURCE_DIRECTORY="."
SOURCE_FILE_TYPE="mkv"
TIMEZONE_OFFSET=$(date +%:::z)
FFMPEG_PARAMETERS="-c:v libx265 -c:a copy"
FINAL_RESTING_PLACE="."
TRASH="~/.local/share/Trash/files/"
FILENAME_REGEX="stthomasglassboro_(2[0-9][0-9][0-9])-([0-1][0-9])-([0-3][0-9])T([0-2][0-9]):([0-5][0-9]):([0-5][0-9])Z"

ffmpeg="$(which ffmpeg)"

report "INFO | Timezone offset = $TIMESZONE_OFFSET"

SOURCE_DIRECTORY=$(realpath "$SOURCE_DIRECTORY")
if [ ! -d "$SOURCE_DIRECTORY" ]; then
	report "ERROR | Abort: cannot reach $SOURCE_DIRECTORY"
	exit 1
fi

FINAL_RESTING_PLACE=$(realpath "$FINAL_RESTING_PLACE")
if [ ! -d "$SOURCE_DIRECTORY" ]; then
	report "ERROR | Abort: cannot reach $FINAL_RESTING_PLACE"
	exit 1
fi

# get lock to affirm I'm exclusive user of this backup directory
exec 200>"$SOURCE_DIRECTORY/lock"
if ! flock -n 200; then
	report "ERROR | Cannot lock directory for exclusive $_self"
	exit 1
fi
# this now runs under the lock until 200 is closed
# (it will be closed automatically when the script ends)
# src: http://mywiki.wooledge.org/BashFAQ/045

for f in $SOURCE_DIRECTORY/*.$SOURCE_FILE_TYPE; do
	[ -n "$DEBUG" ] && report "DEBUG | Working on file $f"
	if [[ $f =~ $FILENAME_REGEX ]]; then
		year=${BASH_REMATCH[1]}
		month=${BASH_REMATCH[2]}
		day=${BASH_REMATCH[3]}
		hour=${BASH_REMATCH[4]}
		minute=${BASH_REMATCH[5]}
		second=${BASH_REMATCH[6]}
	fi
	hour=$(($hour + $TIMEZONE_OFFSET))
	hour=$(printf "%02d" $hour)
	[ -n "$DEBUG" ] && report "DEBUG | year=$year  month=$month  day=$day"
	[ -n "$DEBUG" ] && report "DEBUG | hour=$hour  minute=$minute  second=$second"

	new_name="$FINAL_RESTING_PLACE/StT-$year$month$day-$hour$minute$second.mp4"
	report "INFO | Converting $(basename $f) to $(basename $new_name)"
	if ffmpeg -i $f $FFMPEG_PARAMETERS $new_name; then
		mv $f $TRASH
	fi
done
report "FINISH"
