# logstash start1 - e 옵션
bin/logstash -e '
input { stdin{} }
output { stdout{} }'

# logstash start2 - f 옵션
bin/logstash -f workshop.conf