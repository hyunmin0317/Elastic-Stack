sudo apt install netcat

echo 'Hello Logstash' | nc 10.178.0.5 9900

head -n 1 ./weblog-sample.log | nc 10.178.0.5 9900

bin/logstash-plugin install logstash-codec-es_bulk