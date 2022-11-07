# LOG8415-Assignment-2

Navigate to Azure website: https://azure.microsoft.com/en-ca/
Sign-in with education account

## CREATION OF VM:
On Azure Home, Click on "Create a ressource" under Azure services
Click on "Create" under "Virtual machine"
Choose the following options for the Virtual Machine
In Basics:
- Ressource group: Create new ressource group
- Virtual machine name: 
- Region: US East
- Availability options: No infrastructure redundancy required
- Security type: Standard
- Image: Ubuntu Server 20.04 LTS - Gen2
- VM architecture x86
- Size: Standard_D2s_v3 - 2vcpus, 8GiB memory
- Authentification type: SSH public key
- Username: azureuser
- SSH public key source: Generate new or use one if already created
- Public inbound portst: Allow selected ports
- Select inbound ports: SSH (22)
In Disks:
- Delete with VM: true
In Networking:
- NIC network security group: Basic
- Public inbound ports: Allow selected ports
- Select inbound ports: SSH (22)

The rest of the options are default. Go to Review + Create, click on Create. 
When VM is created, click "Go to ressource", or navigate to home, click on VM name. 
Click "Connect", copy the path of the downloaded Key to the field. Copy the ssh command and paste it in a terminal to connect to the instance. 

## IN THE VM:
run the following commands:
- git clone https://github.com/anthonysarkis/LOG8415-Assignment-2.git
- cd LOG8415-Assignment-2
- chmod +x userdata.sh
- ./userdata.sh
OR run the lines in userdata.sh one by one. 

The pg4300.txt experiment output with Hadoop is in output_pg4300, the time in time_hadoop_pg4300.txt. With Linux, the time is in time_linux_pg4300.txt. The tinyurl datasets output is in output_hadoop_datasets, and the times of the three experiments are in time_hadoop_datasets_1.txt, time_hadoop_datasets_2.txt and time_hadoop_datasets_3.txt. For spark, the outputs are in output_spark_datasets, and the times are in time_spark_datasets_1.txt, time_spark_datasets_2.txt and time_spark_datasets_3.txt. For the friend recommendation experiment, the output is in friends_output folder. 