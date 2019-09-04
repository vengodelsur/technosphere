import org.apache.hadoop.mapreduce.Partitioner;
import org.apache.hadoop.io.IntWritable;

public class HostHashPartitioner extends Partitioner<HostQueryKey, IntWritable> {
    @Override
    public int getPartition(HostQueryKey key,IntWritable value, int numPartitions) {
        return (key.getHost().hashCode() & Integer.MAX_VALUE) % numPartitions;
    }


}