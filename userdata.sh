#!/bin/bash
echo "Apt update"
sudo apt update
echo "Installing Java"
sudo apt-get -y install default-jdk default-jre

echo "Installing Hadoop"
wget https://downloads.apache.org/hadoop/common/hadoop-3.3.1/hadoop-3.3.1.tar.gz
tar -xvzf hadoop-3.3.1.tar.gz
sudo mv hadoop-3.3.1 /usr/local/hadoop
rm -r hadoop-3.3.1.tar.gz

echo "Setting Hadoop environment variables"
export HADOOP_HOME=/usr/local/hadoop
export PATH=$PATH:/usr/local/hadoop/sbin:/usr/local/hadoop/bin
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64

# PG4300.TXT experiment
echo "Wordcount on pg4300.txt with hadoop"
{ time hadoop jar /usr/local/hadoop/share/hadoop/mapreduce/hadoop-mapreduce-examples-3.3.1.jar wordcount pg4300.txt output_pg4300 ; } 2> time_hadoop_pg4300.txt

echo "Wordcount on pg4300.txt with linux cat"
{ time cat pg4300.txt | tr ' ' '\n' | sort | uniq -c ; } 2> time_linux_pg4300.txt