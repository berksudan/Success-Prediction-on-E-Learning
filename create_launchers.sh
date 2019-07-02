#!/bin/sh

APPDIR="$PWD"

create_launcher () {
	app_dir=$1
	launcher_file=$2
	icon_file=$3
	launcher_name=$4
	exec_command=$5
	run_in_terminal=$6
	
	printf "#!/usr/bin/env xdg-open
[Desktop Entry]
Version=1.0
Type=Application
Terminal=$run_in_terminal
Exec=$exec_command
Name[en_US]=$launcher_name
Comment[en_US]=$launcher_name
Icon[en_US]=$icon_file
Name=$launcher_name
Comment=$launcher_name
Icon=$icon_file
Path=$app_dir
	" | tee  $launcher_file > /dev/null

	chmod +x $launcher_file
	echo "-------------------------------------------"
	echo "INFOS ABOUT CREATED FILES:"
	echo "-> Icon File: \"$icon_file\""
	echo "-> Exec Command of Launcher: \"$exec_command\""
	echo "-> Launcher Name: \"$launcher_name\""
	echo "-> Created Launcher File: \"$launcher_file\""
	echo "-------------------------------------------"
}

main(){
	cd $(dirname "$0")
	preprocessor_launcher_file=$APPDIR/RunSparkWebLogPreprocessor.desktop
	preprocessor_icon_file=$APPDIR/.preprocessor_app_logo.png
	preprocessor_launcher_name="Run Spark Web Log Preprocessor"
	preprocessor_exec_command="java -jar $APPDIR/jars/SparkPreprocessor.jar"
	preprocessor_run_in_terminal=false
	create_launcher "$APPDIR" "$preprocessor_launcher_file" "$preprocessor_icon_file" "$preprocessor_launcher_name" "$preprocessor_exec_command" $preprocessor_run_in_terminal
	
	######################################################################
	
	classifier_launcher_file=$APPDIR/RunSparkBinaryClassifier.desktop
	classifier_icon_file=$APPDIR/.binary_classifier_app_logo.png
	classifier_launcher_name="Run Spark Binary Classifier"
	classifier_exec_command="bash -c \"java -jar /home/kubrick/eclipse-workspace/GraduationProject/jars/SparkClassifier.jar; read line\""
	classifier_run_in_terminal=true
	create_launcher "$APPDIR" "$classifier_launcher_file" "$classifier_icon_file" "$classifier_launcher_name" "$classifier_exec_command" $classifier_run_in_terminal
}

main



