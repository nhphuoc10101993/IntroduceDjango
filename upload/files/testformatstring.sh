#/bin/bash
value="192.168.95.11 192.168.95.12 192.168.95.13"
declare -a arr=(`echo $value`)
getIndexFromArray(){
    ip=$1
    getNextIp=""
    index=1
    for ((i=0;i<${#arr[@]};i++));do
        if [ "${arr[$i]}" = "$ip" ];then
            index=`expr $i + 1`
            if [ $index -eq ${#arr[@]} ];then
                getNextIp=${arr[0]}
            else
                getNextIp=${arr[$index]}
                break
            fi
        fi
    done 
    echo $getNextIp
}
getIndexFromArray $@