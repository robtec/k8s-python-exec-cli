#!/bin/bash

echo "Starting verification script"

namespace="hello-test"

data_file="/work/data/test.txt"

if kubectl get ns | grep -i $namespace; then

   echo "Namespace $namespace exists"
   pvc=$(kubectl get pvc -n $namespace | grep -v NAME | awk '{print $1}')
   kubectl patch pvc $pvc -n $namespace -p '{"metadata":{finalizers":null}}' && kubectl delete namespace $namespace
   
   sleep 15
   
   backup_name=$(velero get backups | grep -v NAME | head -n 1 | awk '{print $1}')
   
   velero restore create --from-backup_name --include-namespace $namespace
   
   sleep 30
   
   pod=$(kubbectl get pod -n namespace | grep -v NAME | awk '{print $1}')
   
   current_date=$(date +%d-%m-%Y)
   
   check_data=$(kubectl exec -it $pod -n $namespace -- cat $data_file | grep $current_date | head -n 1)
   
   if [ -z "$check_data" ]
   then
       echo "data is present"
	   
    else 
	   echo "data exists: $check_data"
	fi
	
else
   echo "Namespace or data not present"
fi