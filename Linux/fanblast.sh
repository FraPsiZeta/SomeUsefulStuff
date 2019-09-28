#!/bin/sh

################## Definizione variabili: ##################

max_temp=80
min_temp=60
max_rpm1=6156
max_rpm2=5700
stop_value=0
loop_var=0

trap printout INT
printout() {
	echo ""
	echo "The script was killed, need to get the fan on auto again.."
	if [ $(cat /sys/devices/platform/applesmc.768/fan1_manual) -ne 0 ] || [ $(cat /sys/devices/platform/applesmc.768/fan2_manual) -ne 0 ]  ; then
		echo 0 > /sys/devices/platform/applesmc.768/fan1_manual
		echo 0 > /sys/devices/platform/applesmc.768/fan2_manual
	fi
	stop_value=99
	echo "Done!"
}

#################   Loop Temperature   ##################
while true
do
	curr_temp="$( sensors | grep 'Core 1' | grep -o '[0-9]*' | sed -n '1!p' | head -n1 )"
	real_rpm1=$(echo  " $max_rpm1 - (  ( ( $max_temp-$curr_temp ) / ( $max_temp-$min_temp ) )  * 3800 ) " | bc -l)
	real_rpm1=${real_rpm1%.*}
	real_rpm2=$(echo  " $max_rpm2 - (  ( ( $max_temp-$curr_temp ) / ( $max_temp-$min_temp ) )  * 3550 ) " | bc -l)
	real_rpm2=${real_rpm2%.*}
	#This stops the script after 100 seconds under min_temp
	if [ $stop_value -ge 20 ] ; then
		if [ $(cat /sys/devices/platform/applesmc.768/fan1_manual) -ne 0 ] || [ $(cat /sys/devices/platform/applesmc.768/fan2_manual) -ne 0 ]  ; then
			echo 0 > /sys/devices/platform/applesmc.768/fan1_manual
			echo 0 > /sys/devices/platform/applesmc.768/fan2_manual
		fi
		break
	fi
	#This stop the fans
	if [ $curr_temp -lt $min_temp ] ; then
		stop_value=$((stop_value+1))
		if [ $(cat /sys/devices/platform/applesmc.768/fan1_manual) -ne 0 ] || [ $(cat /sys/devices/platform/applesmc.768/fan2_manual) -ne 0 ]  ; then
			echo 0 > /sys/devices/platform/applesmc.768/fan1_manual
			echo 0 > /sys/devices/platform/applesmc.768/fan2_manual
		fi
	#This spins the fans at max
	elif [ $curr_temp -gt $max_temp ] ; then
		stop_value=0
		echo 1 > /sys/devices/platform/applesmc.768/fan1_manual
		echo 1 > /sys/devices/platform/applesmc.768/fan2_manual
		echo $max_rpm1 > /sys/devices/platform/applesmc.768/fan1_output
		echo $max_rpm2 > /sys/devices/platform/applesmc.768/fan2_output
	#This spins the fans linearly
	elif [ $curr_temp -le $max_temp ] && [ $curr_temp -ge $min_temp ] ; then
		stop_value=0
		if [ $real_rpm1 -gt 2100 ] && [ $real_rpm1 -le 6156 ] && [ $real_rpm2 -gt 2000 ] && [ $real_rpm2 -le 5700 ] ; then 
			echo 1 > /sys/devices/platform/applesmc.768/fan1_manual
			echo 1 > /sys/devices/platform/applesmc.768/fan2_manual
			echo $real_rpm1 > /sys/devices/platform/applesmc.768/fan1_output
			echo $real_rpm2 > /sys/devices/platform/applesmc.768/fan2_output
		else
			echo "Something wrong happened, exiting..."
			if [ $(cat /sys/devices/platform/applesmc.768/fan1_manual) -ne 0 ] || [ $(cat /sys/devices/platform/applesmc.768/fan2_manual) -ne 0 ]  ; then
				echo 0 > /sys/devices/platform/applesmc.768/fan1_manual
				echo 0 > /sys/devices/platform/applesmc.768/fan2_manual
			fi
			break
		fi
	else
		if [ $(cat /sys/devices/platform/applesmc.768/fan1_manual) -ne 0 ] || [ $(cat /sys/devices/platform/applesmc.768/fan2_manual) -ne 0 ]  ; then
			echo 0 > /sys/devices/platform/applesmc.768/fan1_manual
			echo 0 > /sys/devices/platform/applesmc.768/fan2_manual
		fi
		echo "Something wrong happened"
		echo "Exiting..."
		break
	fi		
	if [ $loop_var -eq 0 ] ; then
		echo "##############################################"
	else 
		echo "\033[6A\r##############################################"
	fi
		echo "# Average temperature of the CPU: \033[31m$curr_temp °C\033[0m      #"
		if [ $real_rpm1 -lt 2100 ] || [ $real_rpm2 -lt 2000 ] ; then 
			echo "# Left Fan Speed: \033[31m2100 rpm\033[0m                   #"
			echo "# Right Fan Speed: \033[31m2000 rpm\033[0m                  #"
			echo "# $(( 95 - ( $stop_value * 5 ) )) Seconds until the Script closes itself! #"
			echo "##############################################"
		elif [ $real_rpm1 -gt 6156 ] || [ $real_rpm2 -gt 5700 ] ; then 
			echo "# Left Fan Speed: \033[31m6156 rpm\033[0m                   #"
			echo "# Right Fan Speed: \033[31m5700 rpm\033[0m                  #"
			echo "# Running...                                 #"
			echo "##############################################"
		else
			echo "# Left Fan Speed: \033[31m$real_rpm1 rpm\033[0m                   #"
			echo "# Right Fan Speed: \033[31m$real_rpm2 rpm\033[0m                  #"
			echo "# Running...                                 #"
			echo "##############################################"
		fi
	sleep 5
	loop_var=$((loop_var+1))
done
