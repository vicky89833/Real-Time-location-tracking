1996  KAFKA_CLUSTER_ID="$(bin/kafka-storage.sh random-uuid)"
 1997  bin/kafka-storage.sh format --standalone -t $KAFKA_CLUSTER_ID -c config/server.properties
 1998  bin/kafka-server-start.sh config/server.properties
